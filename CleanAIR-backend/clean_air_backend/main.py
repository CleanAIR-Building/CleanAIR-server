#!/usr/bin/python3
from data_processing.entities.limit import store_limits
from data_processing.consumers.carbon_dioxide_consumer import CarbonDioxideConsumer
from data_processing.consumers.infrared_consumer import InfraRedConsumer
from data_processing.consumers.photoelectric_barrier_consumer import PhotoelectricBarrierConsumer
from data_processing.consumers.traffic_light_consumer import TrafficLightConsumer
from data_processing.consumers.window_state_consumer import WindowStateConsumer
from data_processing.session import create_database_session
from data_processing.system_state import SystemState
from mqtt.mqtt_client import MQTTClient
from orchestration.orchestration import Orchestrator
from planning.clean_air_building import BuildingState
from planning.smart_building_logic import SmartBuildingLogic
from config.config import config
import logging
import os

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    # Setup database
    logger.info("Started CleanAIR-backend")
    database_config: dict = config("postgresql")
    url: str = "postgresql://{user}:{password}@{host}:{port}/{database}".format(
        user=os.environ.get("POSTGRES_USER", database_config["user"] if "user" in database_config else "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD",
                                database_config["password"] if "password" in database_config else "changeme"),
        host=os.environ.get("POSTGRES_HOST", database_config["host"] if "host" in database_config else "localhost"),
        port=os.environ.get("POSTGRES_PORT", database_config["port"] if "port" in database_config else 5432),
        database=os.environ.get("POSTGRES_DATABASE",
                                database_config["database"] if "database" in database_config else "cleanair_data")
    )

    logger.debug(url)
    Session, engine = create_database_session(url)

    # Setup mqtt client
    mqtt_config: dict = config("mqtt")
    mqtt_client: MQTTClient = MQTTClient(
        client_name=os.environ.get("MQTT_CLIENT_NAME",
                                   mqtt_config["client_name"] if "client_name" in mqtt_config else "data_processing12"),
        user=os.environ.get("MQTT_USER", mqtt_config["user"] if "client_name" in mqtt_config else "user1"),
        password=os.environ.get("MQTT_PASSWORD", mqtt_config["password"] if "client_name" in mqtt_config else "user1"),
        host=os.environ.get("MQTT_HOST", mqtt_config["host"] if "client_name" in mqtt_config else "localhost"))

    # Setup Orchestration
    orchestrator: Orchestrator = Orchestrator(mqtt_client)
    sbl = SmartBuildingLogic(BuildingState(), orchestrator)
    system_state: SystemState = SystemState(sbl)

    # Setup message consumers
    infra_red_consumer_config = config("infrared")
    infra_red_consumer: InfraRedConsumer = InfraRedConsumer(topic=infra_red_consumer_config["topic"],
                                                            Session=Session,
                                                            system_state=system_state)

    carbon_dioxide_consumer_config = config("co2")
    carbon_dioxide_consumer: CarbonDioxideConsumer = CarbonDioxideConsumer(
        topic=carbon_dioxide_consumer_config["topic"],
        Session=Session,
        system_state=system_state,
        limit=float(carbon_dioxide_consumer_config["limit"]))

    traffic_light_consumer_config = config("traffic_light")
    traffic_light_consumer: TrafficLightConsumer = TrafficLightConsumer(topic=traffic_light_consumer_config["topic"],
                                                                        Session=Session,
                                                                        system_state=system_state)

    window_state_consumer_config = config("window_state")
    window_state_consumer: WindowStateConsumer = WindowStateConsumer(topic=window_state_consumer_config["topic"],
                                                                     Session=Session,
                                                                     system_state=system_state)

    occupancy_consumer_config = config("occupancy")
    photoelectric_barrier_consumer: PhotoelectricBarrierConsumer = PhotoelectricBarrierConsumer(
        topic=occupancy_consumer_config["topic"],
        Session=Session,
        system_state=system_state,
        limit=int(occupancy_consumer_config["limit"]))

    # Store limits in database
    store_limits(Session=Session,
                 co2_limit=float(carbon_dioxide_consumer_config["limit"]),
                 occupation_limit=float(occupancy_consumer_config["limit"]))

    # Add consumers to mqtt client
    mqtt_client.add_consumer(infra_red_consumer,
                             carbon_dioxide_consumer,
                             traffic_light_consumer,
                             window_state_consumer,
                             photoelectric_barrier_consumer)

    # Connect to mqtt
    mqtt_client.connect()
    mqtt_client.start()
    input()


if __name__ == '__main__':
    main()
