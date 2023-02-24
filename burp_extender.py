from burp import IBurpExtender, IContextMenuFactory, ITab

from java.util import LinkedList
from javax.swing import JMenuItem
from java.awt.event import ActionListener


class MenuImpl(IContextMenuFactory):
    def __init__(self, extender):
        self._extender = extender
        

    def createMenuItems(self, invocation):
        # create a menu with one item (right click inside request/response field)
        ret = LinkedList()
        testItem = JMenuItem("Testitem")

        # add an action
        testItem.addActionListener(HandleMenuItems(self._extender))
        ret.add(testItem)
        return ret


class HandleMenuItems(ActionListener):
    def __init__(self, extender):
        self._extender = extender
    
    def actionPerformed(self, e):
        # print to stdout if menu item is clicked
        self._extender._callbacks.printOutput("Action performed!")


class ITabImpl(ITab):
    def __init__(self, extender):
        self._extender = extender

    def getTabCaption(self):
        # set name of your extension tab
        return "<Your-TabCaption>"

    def getUiComponent(self):
        # return your extension page
        self._txtInput = self._extender._callbacks.createTextEditor()
        self._txtInput.setEditable(True)
        return self._txtInput.getComponent()


class BurpExtender(IBurpExtender):
    def registerExtenderCallbacks(self, callbacks):
        # name your extension
        callbacks.setExtensionName("<Your-Extensionname>")

        # save helper and callback function
        self._helpers = callbacks.getHelpers()
        self._callbacks = callbacks  

        # print to extension stdout
        callbacks.printOutput("Hello World!")

        # register context menu
        callbacks.registerContextMenuFactory(MenuImpl(self))
        # register new tab
        callbacks.addSuiteTab(ITabImpl(self))

