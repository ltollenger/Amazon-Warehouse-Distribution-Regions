This project's goal is to use python to create distribution regions for a select number of Amazon warehouses [[1]] based on each location's approximate distance to all the US ZIP codes found within a mock western sales region. The python code
provided creates a CSV file that matches each ZIP code in the west sales region to the closest distribution center.  A business application using this data could be to determine if distribution centers are too close to one another based on the number ZIP
codes the distribution center serves.  For example, LAS2 and LAS6 are favorable locations in terms of distance for only 43 and 151 ZIP codes respectively out the total 5357 ZIP codes in the western saels region.  This information tells us that, in terms 
of ZIP codes served, the location of Amazon warehouses could be optimized.

[1]: https://warehousegig.com/blog/amazon-fulfillment-warehousing-locations
