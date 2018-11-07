# brewfather plugin for CraftBeerPi 3.0
Update Brewfather batch fermentation data from CraftBeerPi3 Tilt devices. Currently the code handles RED and PINK Tilt devices.

## IMPORTANT NOTE
The handling of Tilt connectivity has changed in the latest releases of BrewFather (for the better). It now can allocate the Tilt to a Batch at the BrewFather end. This means that this module no longer needs to allocate a Batch Number to a Tilt at the craftbeerpi end. I think this means that it can now work for any number of Tilts and regardless of Colour, just do all the set up at the BrewFather end and send the data from craftbeerpi leaving the Beer Name/Batch Number field blank. I am testing this over the next few days and will probably just remove the unnecessary parameter fields in an update.

## Pre-requisites
Brewfather https://web.brewfather.app

CraftBeerPi 3.0 https://github.com/Manuel83/craftbeerpi3

## Configuration for CraftBeerPi
1. In CraftBeerPi3 set up each Tilt as a pair of sensors, one for Temperature immediately followed by the same Tilt for Gravity
2. Make sure the devices are reporting data to CraftBeerPi3
3. Download this plugin into the craftbeerpi3/modules/plugins directory and restart CraftBeerPi3

## CraftBeerPi3 Parameters
1. Set parameter brewfather_COLOR_beer (where COLOR is RED, PINK, etc.) as the Batch Number for the beer as allocated in Brewfather
2. Set brewfather_comment to the text you would like to appear along with the reading details (e.g. "Posted from CraftBeerPi 3.0")
3. Set the brewfather_id to the text that follows the ?id= text in the Cloud URL on the Brewfather / Settings / Utility / Tilt Hydrometer
   It will look something like "4ZXbnm8TY7asdf"

## Results
1. Logging occurs every 15 minutes. Wait a while for some values to log.
2. Go to the Fermenting tab of the Brewfather Batches for the relevant batch. The graph will show logged temperature and Gravity values
3. The Edit button will show individual logged results and the comment.

## Improvements
At the moment it only caters for RED and PINK Tilt devices as those are the ones I have. It's not hard to alter the code to change those to your devices or even add more.
