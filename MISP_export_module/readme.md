The idea would be to use the system developped during the master thesis directly inside the misp system.

The first step is to create a module that allows to transform events one by one. This is interesting at first but has some disadvantages:
- As it is event by event, we cannot use the bloomy (bloom filter) system
- As it is event by evenet, we cannot directly generate separate file in function of the type of the IOC

Another disadvantage with the actual modules is that we only have access to standard data while the advantage of this system could be to allow some more cooperation. For example, some companies could add information and only accept to share in this format as it reveals the information only if the user has already some knowledges of it.