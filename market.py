# for printing snapshot 
NO_CHANGE = 0 
PRICE_CHANGE = 1  
VOLUME_CHANGE = 2 

BUY = 0
SELL = 1

class Price(object):
    # takes 1 order as input
    def __init__(self, price, volume, order_id):
        # Price part
        self.price = price
        self.total_volume = volume
        self.orders = { order_id : volume} # order_id : volume

        # Tree part
        self.left = None
        self.right = None
        self.height = 1
 

# AVL tree class which supports insertion and deletion operations
class AVL_Tree(object):
    def insert(self, root, price, volume, order_id, price_map):
         
        if not root:
            new_price_node = Price(price, volume, order_id)
            price_map[price] = new_price_node
            return new_price_node
        elif price < root.price:
            root.left = self.insert(root.left, price, volume, order_id, price_map)
        else:
            root.right = self.insert(root.right, price, volume, order_id, price_map)
 
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
 
        balance = self.getBalance(root)
 
        if balance > 1 and price < root.left.price:
            return self.rightRotate(root)
 
        if balance < -1 and price > root.right.price:
            return self.leftRotate(root)

        if balance > 1 and price > root.left.price:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        if balance < -1 and price < root.right.price:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root
 
    def delete(self, root, price):
 
        if not root:
            return root
 
        elif price < root.price:
            root.left = self.delete(root.left, price)
 
        elif price > root.price:
            root.right = self.delete(root.right, price)
 
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
 
            elif root.right is None:
                temp = root.left
                root = None
                return temp
 
            temp = self.getMinPriceNode(root.right)
            root.price = temp.price
            root.right = self.delete(root.right, temp.price)
 
        if root is None:
            return root
 
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
 
        balance = self.getBalance(root)
 
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
 
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
 
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root
 
    def leftRotate(self, pivotNode):
        newRoot = pivotNode.right
        leftSubtreeOfNewRoot = newRoot.left
 
        newRoot.left = pivotNode
        pivotNode.right = leftSubtreeOfNewRoot
 
        pivotNode.height = 1 + max(self.getHeight(pivotNode.left), self.getHeight(pivotNode.right))
        newRoot.height = 1 + max(self.getHeight(newRoot.left), self.getHeight(newRoot.right))
 
        return newRoot
 
    def rightRotate(self, pivotNode):
        newRoot = pivotNode.left
        rightSubtreeOfPivot = newRoot.right
 
        newRoot.right = pivotNode
        pivotNode.left = rightSubtreeOfPivot
 
        pivotNode.height = 1 + max(self.getHeight(pivotNode.left), self.getHeight(pivotNode.right))
        newRoot.height = 1 + max(self.getHeight(newRoot.left), self.getHeight(newRoot.right))
 
        return newRoot
 
    def getHeight(self, root):
        if not root:
            return 0
 
        return root.height
 
    def getBalance(self, root):
        if not root:
            return 0
 
        return self.getHeight(root.left) - self.getHeight(root.right)
 
    def getMinPriceNode(self, root):
        if root is None or root.left is None:
            return root
 
        return self.getMinPriceNode(root.left)
 
    def inOrderTraversalSnapshot(self, root, topNList, N):
 
        # Check if root is None or we have enough elements
        if not root or len(topNList) == N:
            return
        
        self.inOrderTraversalSnapshot(root.left, topNList, N)

        # see if we have enough again
        if len(topNList) == N:
            return
        
        topNList.append((root.price, root.total_volume))

        # see if we have enough again
        if len(topNList) == N:
            return

        self.inOrderTraversalSnapshot(root.right, topNList, N)

    def inOrderTraversalReverseSnapshot(self, root, topNList, N):
 
        # Check if root is None or we have enough elements
        if not root or len(topNList) == N:
            return
        
        self.inOrderTraversalReverseSnapshot(root.right, topNList, N)

        # see if we have enough again
        if len(topNList) == N:
            return
        
        topNList.append((root.price, root.total_volume))

        # see if we have enough again
        if len(topNList) == N:
            return

        self.inOrderTraversalReverseSnapshot(root.left, topNList, N)
        
 
class Symbol(object):
    def __init__(self, N):
        self.avl_tree = AVL_Tree()
        
        self.N = N

        self.bids = None                    # AVL Tree root
        self.bids_price_map = dict()        # price : Price
        self.bids_order_id_map = dict()     # order_id : Price
        self.nth_bid_price = None
        self.last_bid_snapshot_str = "[]"
        self.last_bid_snapshot_list = []

        self.asks = None                    # AVL Tree root
        self.asks_price_map = dict()        # price : Price
        self.asks_order_id_map = dict()     # order_id : price
        self.nth_ask_price = None
        self.last_ask_snapshot_str = "[]"
        self.last_ask_snapshot_list = []

    def newSnapshotBuy(self):
        # get new decreasing list of prices and volumes for snapshot
        self.last_bid_snapshot_list = [] # reset list
        self.avl_tree.inOrderTraversalReverseSnapshot(self.bids, self.last_bid_snapshot_list, self.N)
        
        # change nth_bid_price
        if len(self.last_bid_snapshot_list) < self.N:
            self.nth_bid_price = None
        else:
            self.nth_bid_price = self.last_bid_snapshot_list[-1][0] # from (price, volume)

        self.changeSnapshotString(BUY)

    def newSnapshotSell(self):
        # get new increasing list of prices and volumes for snapshot
        self.last_ask_snapshot_list = [] # reset list
        self.avl_tree.inOrderTraversalSnapshot(self.asks, self.last_ask_snapshot_list, self.N)
        
        # change nth_ask_price
        if len(self.last_ask_snapshot_list) < self.N:
            self.nth_ask_price = None
        else:
            self.nth_ask_price = self.last_ask_snapshot_list[-1][0] # from (price, volume)
        
        self.changeSnapshotString(SELL)

    def changeSnapshotString(self, orderType):
        if orderType == BUY:
            self.last_bid_snapshot_str = self.convertSnapshotToString(self.last_bid_snapshot_list)
        elif orderType == SELL:
            self.last_ask_snapshot_str = self.convertSnapshotToString(self.last_ask_snapshot_list)

    def convertSnapshotToString(self, snapshot_list):
        snapshot_str = "[" + ", ".join(f"({price}, {volume})" for price, volume in snapshot_list) + "]"
        return snapshot_str

    def editSnapshotBuy(self, editPrice, newVolume):
        for index, (price, volume) in enumerate(self.last_bid_snapshot_list):
            if price == editPrice:
                self.last_bid_snapshot_list[index] = (price, newVolume)
        self.changeSnapshotString(BUY)

    def editSnapshotSell(self, editPrice, newVolume):
        for index, (price, volume) in enumerate(self.last_ask_snapshot_list):
            if price == editPrice:
                self.last_ask_snapshot_list[index] = (price, newVolume)
        self.changeSnapshotString(SELL)

    def edit2SnapshotBuy(self, editPrice1, newVolume1, editPrice2, newVolume2):
        for index, (price, volume) in enumerate(self.last_bid_snapshot_list):
            if price == editPrice1:
                self.last_bid_snapshot_list[index] = (price, newVolume1)
            elif price == editPrice2:
                self.last_bid_snapshot_list[index] = (price, newVolume2)
        self.changeSnapshotString(BUY)

    def edit2SnapshotSell(self, editPrice1, newVolume1, editPrice2, newVolume2):
        for index, (price, volume) in enumerate(self.last_ask_snapshot_list):
            if price == editPrice1:
                self.last_ask_snapshot_list[index] = (price, newVolume1)
            elif price == editPrice2:
                self.last_ask_snapshot_list[index] = (price, newVolume2)
        self.changeSnapshotString(SELL)

    def add(self, side, price, volume, order_id):
        if side == 'B':
            change = self.addBuy(price, volume, order_id)
            if change == NO_CHANGE:
                return None
            elif change == VOLUME_CHANGE:
                newVolume = self.bids_order_id_map[order_id].total_volume
                self.editSnapshotBuy(price, newVolume)
            elif change == PRICE_CHANGE:
                self.newSnapshotBuy()
        elif side == 'S':
            change = self.addSell(price, volume, order_id)
            if change == NO_CHANGE:
                return None
            elif change == VOLUME_CHANGE:
                newVolume = self.asks_order_id_map[order_id].total_volume
                self.editSnapshotSell(price, newVolume)
            elif change == PRICE_CHANGE:
                self.newSnapshotSell()
        return (self.last_bid_snapshot_str, self.last_ask_snapshot_str) # bids, asks

    def addBuy(self, price, volume, order_id):
        # volume change only
        if price in self.bids_price_map:
            self.bids_price_map[price].total_volume += volume # change volume
            self.bids_price_map[price].orders[order_id] = volume # add order_id
            self.bids_order_id_map[order_id] = self.bids_price_map[price] # add order id map
            if self.nth_bid_price == None or price >= self.nth_bid_price:
                return VOLUME_CHANGE
            else: 
                return NO_CHANGE
        # price change
        else:
            # insert
            self.bids = self.avl_tree.insert(self.bids, price, volume, order_id, self.bids_price_map)
            self.bids_order_id_map[order_id] = self.bids_price_map[price] # add order id map
            # insertion changed snapshot
            if self.nth_bid_price == None or price > self.nth_bid_price:
                return PRICE_CHANGE
            else:
                return NO_CHANGE

    def addSell(self, price, volume, order_id):
        # volume change only
        if price in self.asks_price_map:
            self.asks_price_map[price].total_volume += volume # change volume
            self.asks_price_map[price].orders[order_id] = volume # add order_id
            self.asks_order_id_map[order_id] = self.asks_price_map[price] # add order id map

            if self.nth_ask_price == None or price <= self.nth_ask_price:
                return VOLUME_CHANGE
            else:
                return NO_CHANGE
        # price change
        else:
            # insert
            self.asks = self.avl_tree.insert(self.asks, price, volume, order_id, self.asks_price_map)
            self.asks_order_id_map[order_id] = self.asks_price_map[price] # add order id map
            # check if insertion changed snapshot
            if self.nth_ask_price == None or price < self.nth_ask_price:
                return PRICE_CHANGE
            else:
                return NO_CHANGE

    def update(self, side, price, volume, order_id):
        if side == 'B':
            # new price doesnt change from old price
            priceNodeOld = self.bids_order_id_map[order_id]
            if priceNodeOld.price == price:
                # equivalent to exectute if volume + execute = old_volume or execute = old_volume - volume
                return self.execute(side, priceNodeOld.orders[order_id] - volume, order_id)
            
            changeDelete, changeAdd = self.updateBuy(price, volume, order_id)
            if changeDelete == NO_CHANGE and changeAdd == NO_CHANGE:
                return None
            elif changeAdd == PRICE_CHANGE or changeDelete == PRICE_CHANGE:
                self.newSnapshotBuy()
            elif changeAdd == VOLUME_CHANGE and changeDelete == VOLUME_CHANGE:
                newVolume1 = self.bids_price_map[priceNodeOld.price].total_volume
                newVolume2 = self.bids_price_map[price].total_volume
                self.edit2SnapshotBuy(priceNodeOld.price, newVolume1, price, newVolume2)
            elif changeAdd == NO_CHANGE:
                newVolume = self.bids_price_map[priceNodeOld.price].total_volume
                self.editSnapshotBuy(priceNodeOld.price, newVolume)
            elif changeDelete == NO_CHANGE:
                newVolume = self.bids_price_map[price].total_volume
                self.editSnapshotBuy(price, newVolume)

        elif side == 'S':
            # new price doesnt change from old price
            priceNodeOld = self.asks_order_id_map[order_id]
            if priceNodeOld.price == price:
                # equivalent to exectute if volume + execute = old_volume or execute = old_volume - volume
                return self.execute(side, priceNodeOld.orders[order_id] - volume, order_id)
            
            changeDelete, changeAdd = self.updateSell(price, volume, order_id)
            if changeDelete == NO_CHANGE and changeAdd == NO_CHANGE:
                return None
            elif changeAdd == PRICE_CHANGE or changeDelete == PRICE_CHANGE:
                self.newSnapshotSell()
            elif changeAdd == VOLUME_CHANGE and changeDelete == VOLUME_CHANGE:
                newVolume1 = self.asks_price_map[priceNodeOld.price].total_volume
                newVolume2 = self.asks_price_map[price].total_volume
                self.edit2SnapshotSell(priceNodeOld.price, newVolume1, price, newVolume2)
            elif changeAdd == NO_CHANGE:
                newVolume = self.asks_price_map[priceNodeOld.price].total_volume
                self.editSnapshotSell(priceNodeOld.price, newVolume)
            elif changeDelete == NO_CHANGE:
                newVolume = self.asks_price_map[price].total_volume
                self.editSnapshotSell(price, newVolume)

        return (self.last_bid_snapshot_str, self.last_ask_snapshot_str) # bids, asks

    def updateBuy(self, price, volume, order_id):
        # price must change

        # delete order and add order again
        # need to keep track of price that got deleted
        # need to keep track of price that got added
        
        deleteChange = self.deleteBuy(order_id)
        addChange = self.addBuy(price, volume, order_id)
        return (deleteChange, addChange)

    def updateSell(self, price, volume, order_id):
        # price must change

        # delete order and add order again
        # need to keep track of price that got deleted
        # need to keep track of price that got added
        
        deleteChange = self.deleteSell(order_id)
        addChange = self.addSell(price, volume, order_id)
        return (deleteChange, addChange)

    def delete(self, side, order_id):
        if side == 'B':
            price = self.bids_order_id_map[order_id].price
            change = self.deleteBuy(order_id)
            if change == NO_CHANGE:
                    return None
            elif change == VOLUME_CHANGE:
                newVolume = self.bids_price_map[price].total_volume # will work because we know price inst deleted
                self.editSnapshotBuy(price, newVolume) 
            elif change == PRICE_CHANGE:
                self.newSnapshotBuy()
        elif side == 'S':
            price = self.asks_order_id_map[order_id].price
            change = self.deleteSell(order_id)
            if change == NO_CHANGE:
                return None
            elif change == VOLUME_CHANGE:
                newVolume = self.asks_price_map[price].total_volume # will work because we know price inst deleted
                self.editSnapshotSell(price, newVolume) 
            elif change == PRICE_CHANGE:
                self.newSnapshotSell()
        return (self.last_bid_snapshot_str, self.last_ask_snapshot_str) # bids, asks
           
    def deleteBuy(self, order_id):
        # delete order
        priceNode = self.bids_order_id_map[order_id]
        priceNode.total_volume -= priceNode.orders[order_id] # change volume
        del priceNode.orders[order_id] # delete order_id
        del self.bids_order_id_map[order_id] # delete order_id
        price = priceNode.price # get price

        # price change
        if priceNode.total_volume == 0:
            # delete node
            self.bids = self.avl_tree.delete(self.bids, price)
            del self.bids_price_map[price]
            if self.nth_bid_price == None or price >= self.nth_bid_price:
                return PRICE_CHANGE
            else:
                return NO_CHANGE
        # volume change only
        elif self.nth_bid_price == None or price >= self.nth_bid_price:
            return VOLUME_CHANGE
        else:
            return NO_CHANGE

    def deleteSell(self, order_id):
        # delete order
        priceNode = self.asks_order_id_map[order_id]
        priceNode.total_volume -= priceNode.orders[order_id] # change volume
        del priceNode.orders[order_id] # delete order_id
        del self.asks_order_id_map[order_id] # delete order_id
        price = priceNode.price # get price

        # price change
        if priceNode.total_volume == 0:
            # delete node
            self.asks = self.avl_tree.delete(self.asks, price)
            del self.asks_price_map[price]
            if self.nth_ask_price == None or price <= self.nth_ask_price:
                return PRICE_CHANGE
            else:
                return NO_CHANGE
        # volume change only
        elif self.nth_ask_price == None or price <= self.nth_ask_price:
            return VOLUME_CHANGE
        else:
            return NO_CHANGE
    
    def execute(self, side, volume, order_id):
        if side == 'B':
            price = self.bids_order_id_map[order_id].price # get before in case deleted
            change = self.executeBuy(volume, order_id)
            if change == NO_CHANGE:
                    return None
            elif change == VOLUME_CHANGE:
                newVolume = self.bids_price_map[price].total_volume
                self.editSnapshotBuy(price, newVolume)
            elif change == PRICE_CHANGE:
                self.newSnapshotBuy()
        elif side == 'S':
            price = self.asks_order_id_map[order_id].price # get before in case deleted            
            change = self.executeSell(volume, order_id)
            if change == NO_CHANGE:
                return None
            elif change == VOLUME_CHANGE:
                newVolume = self.asks_price_map[price].total_volume
                self.editSnapshotSell(self.asks_order_id_map[order_id].price, newVolume)
            elif change == PRICE_CHANGE:
                self.newSnapshotSell()
        return (self.last_bid_snapshot_str, self.last_ask_snapshot_str) # bids, asks        
            
    def executeBuy(self, volume, order_id):
        # change volumes
        priceNode = self.bids_order_id_map[order_id] # get price node
        priceNode.total_volume -= priceNode.orders[order_id] # subtract original order volume
        newVolume = priceNode.orders[order_id] - volume # get new calculated volume for order
        priceNode.orders[order_id] = newVolume # change volume of order
        priceNode.total_volume += newVolume # add volume to total volume
        price = priceNode.price # get price in case deletion

        # delete order
        if priceNode.orders[order_id] == 0:
            del priceNode.orders[order_id] # delete order_id
            del self.bids_order_id_map[order_id] # delete order_id
            
            # delete price
            if priceNode.total_volume == 0:
                self.bids = self.avl_tree.delete(self.bids, price)
                del self.bids_price_map[price]
                
                if self.nth_bid_price == None or price >= self.nth_bid_price:
                    return PRICE_CHANGE
                else:
                    return NO_CHANGE

        # volume change only
        elif self.nth_bid_price == None or price >= self.nth_bid_price:
            return VOLUME_CHANGE
        else:
            return NO_CHANGE

    def executeSell(self, volume, order_id):
        # change volumes
        priceNode = self.asks_order_id_map[order_id]
        priceNode.total_volume -= priceNode.orders[order_id] # change volume 
        newVolume = priceNode.orders[order_id] - volume
        priceNode.orders[order_id] = newVolume # change volume
        priceNode.total_volume += newVolume
        price = priceNode.price # get price in case deletion

        
        # delete order
        if priceNode.orders[order_id] == 0:
            del priceNode.orders[order_id] # delete order_id
            del self.asks_order_id_map[order_id] # delete order_id
            
            # delete price
            if priceNode.total_volume == 0:
                self.asks = self.avl_tree.delete(self.asks, price)
                del self.asks_price_map[price]
                
                if self.nth_ask_price == None or price <= self.nth_ask_price:
                    return PRICE_CHANGE
                else:
                    return NO_CHANGE

        elif self.nth_ask_price == None or price <= self.nth_ask_price:
            return VOLUME_CHANGE
        else:
            return NO_CHANGE