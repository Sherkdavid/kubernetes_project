# kubernetes_project
Kubernetes configuration for a twitter streaming microservices architecture. Designed to be scalable at points of data production and consumption.

Microservices are outlined as follows: 

Stream
Streams data from top twitter trend feed. Publishes as message to rabbitMQ

RSS
Fetches data from BBC News RSS and publishes as message to rabbitMQ

RabbitMQ
Queues messages for consumption

Process
Processes messages from the queue for their polarity. Publishes to seperate queue in the rabbitMQ container.

DBPoi
Consumes messages for polarity. Point of interface for database entry.

Redis
Database container
