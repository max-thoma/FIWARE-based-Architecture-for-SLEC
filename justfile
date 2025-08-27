
# start all necessary services
[working-directory: 'docker']
start:
    @docker compose build
    @docker compose create
    @docker compose up -d
    @echo "Give container some extra time to start up"
    @sleep 10
    @echo "✅ Container started"

# stop and remove services, delete the crate-db volume
[working-directory: 'docker']
clean:
    @docker compose down
    @docker volume rm docker_crate-db

# run the co-simulation scenario that is selceted in src/scenario.py file
sim: start provision
    @poetry run python src/scenario.py
    
# configure all services for simulation
[working-directory: 'docker']
provision:
    @sh provision/00_lec_entities_part_1.sh
    @sleep 0.5
    @sh provision/01_lec_entities_part_2.sh
    @sleep 0.5
    @sh provision/02_service_group_wwt.sh
    @sleep 0.5
    @sh provision/03_service_group_pv.sh
    @sleep 0.5
    @sh provision/04_service_group_em.sh
    @sleep 0.5
    @sh provision/05_provision_pv.sh
    @sleep 0.5
    @sh provision/06_provision_em.sh
    @sleep 0.5
    @sh provision/07_provision_wwt.sh
    @sleep 0.5
    @sh provision/08_subscribe_optimizer_pv.sh
    @sleep 0.5
    @sh provision/09_subscribe_ql_wwt.sh
    @sleep 0.5
    @sh provision/10_subscribe_ql_pv.sh
    @sleep 0.5
    @sh provision/11_subscribe_ql_em.sh
    @sleep 0.5
    
    @echo "✅ services are provisioned and configured"
    
install:
    @poetry install