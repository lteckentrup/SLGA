var lsib = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017"),
    roi = 
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[112.20272355518692, -9.188607131443472],
          [112.20272355518692, -44.15049003535831],
          [154.39022355518694, -44.15049003535831],
          [154.39022355518694, -9.188607131443472]]], null, false);

#### You need to update 'SOC' this is the variable you want
var dataset = ee.ImageCollection('CSIRO/SLGA')
                  .filter(ee.Filter.eq('attribute_code', 'SOC'));

### You need to update 'SOC_100_200_EV', this is the name of the dataset
var soilVar = dataset.select('SOC_100_200_EV').toBands();

var crsTransform = [0.1,0,-180,0,-0.1,90];

var geometry = ee.Geometry.Rectangle([112, 39.8412, 116.4849, 40.01236]);
var out_proj = ee.Projection("EPSG:4326", crsTransform)

### Export folder
var export_folder = "Soil";

Map.addLayer(soilVar,null,'test',false)

Export.image.toDrive({
  image: soilVar,
  description: 'get_soil',
  folder: 'Soil',
  region:roi, // Box around Oz
  crs:'EPSG:4326',
  crsTransform: crsTransform
});
