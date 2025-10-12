#!/bin/sh
docker exec -it mongo mongosh -u $1 -p $2 --authenticationDatabase admin --eval "rs.initiate({
 _id: "rs0",
 members: [
   {_id: 0, host: "db"}
 ]
})"