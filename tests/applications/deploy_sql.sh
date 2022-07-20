MSQL_NS=mysql-persistent
wget https://gitlab.consulting.redhat.com/iberia-consulting/inditex/ocs/ocs-procedures/-/raw/master/resources/files/oadp/mysql/mysql-persistent-template.yaml -O mysql-persistent-template.yaml
oc create -f mysql-persistent-template.yaml
wget -qO- https://downloads.mysql.com/docs/world-db.tar.gz | tar xvz  -C /tmp/mysql/
oc -n $MSQL_NS rsync /tmp/mysql/world-db/ $(oc -n $MSQL_NS get pods -o name):/tmp/
oc -n $MSQL_NS rsh $(oc get pods -n $MSQL_NS -o name) mysql -u root -e "source /tmp/world.sql; show schemas;"