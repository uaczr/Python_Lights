import time
from LLCommunicator import LLSignalToReaction, LLReaction, LLSignal, LLSubscription, LLTopic, LLCommunicator, LLSignalToReactionEntry

class LLReactionOnClicked(LLReaction):
    def __init__(self, name, communicator):
        super(LLReactionOnClicked, self).__init__(name)
        self.communicator = communicator

    def react(self, signal):
        print("Clicked On")
        topic = LLTopic("clicked", "1")
        self.communicator.publish(topic)


if __name__ == "__main__":
    signal2reaction = LLSignalToReaction()
    communicator = LLCommunicator("127.0.0.1", 1883)

    subscription_clicked = LLSubscription("clicked", "clicked", signal2Reaction=signal2reaction)
    reaction_clicked = LLReactionOnClicked("clicked", communicator)
    signal2reactionlist = []
    entry1 = LLSignalToReactionEntry(subscription_clicked, reaction_clicked)
    signal2reactionlist.append(entry1)
    signal2reaction.setSignal2ReactionList(signal2reactionlist)


    communicator.connect()

    communicator.addSubscription(subscription_clicked)

    while(True):
        time.sleep(1)

