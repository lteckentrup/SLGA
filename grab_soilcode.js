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
          
var dataset = ee.ImageCollection('CSIRO/SLGA')
                  .filter(ee.Filter.eq('attribute_code', 'SOC'));
var soilDepth = dataset.select('SOC_100_200_EV').toBands();
var crsTransform = [0.25,0,-180,0,-0.25,90];

var geometry = ee.Geometry.Rectangle([112, 39.8412, 116.4849, 40.01236]);
var out_proj = ee.Projection("EPSG:4326", crsTransform)

var export_folder = "Soil";

Map.addLayer(soilDepth,null,'test',false)

Export.image.toDrive({
  // All tiles that intersect the region get exported in their entirety.
  // Clip the image to prevent low resolution tiles from appearing outside
  // of the region.
  image: soilDepth,
  description: 'get_soil',
  folder: 'Soil',
  region:roi, // Box around Oz
  crs:'EPSG:4326',
  crsTransform: crsTransform
});
