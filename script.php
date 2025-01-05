<?php

/* Configuration - Start */
$start_zoom = 15;
$end_zoom = 19;

$start_latitude = 13.06637;
$start_longitude = 80.23895;

$end_latitude = 13.05991;
$end_longitude = 80.24551;

$folder = "./tiles";

/* Configuration - End */

// With markers
//$url = "https://mt0.google.com/vt/lyrs=y&hl=en&x=x_value&y=y_value&z=z_value";

// Satellite image only
$url = "https://mt0.google.com/vt/lyrs=s&hl=en&x=x_value&y=y_value&z=z_value";

for ($z = $start_zoom; $z <= $end_zoom; $z++) {
    $z_folder = $folder."/".$z;
    if (!is_dir($z_folder)) mkdir($z_folder);
    $start_x = getXTile($start_longitude, $z);
    $end_x = getXTile($end_longitude, $z);
    $start_y = getYTile($start_latitude, $z);
    $end_y = getYTile($end_latitude, $z);

    echo "Start X: ".$start_x."\n";
    echo "End X: ".$end_x."\n";
    echo "Start Y: ".$start_y."\n";
    echo "End Y: ".$end_y."\n";

    for ($x = $start_x; $x <= $end_x; $x++) {
        for ($y = $start_y; $y <= $end_y; $y++) {
            $x_folder = $z_folder.'/'.$x;
            if (!is_dir($x_folder)) mkdir($x_folder);
            $y_file = $x_folder.'/'.$y.'.jpg';
            $tile_url = str_replace('x_value',$x,$url);
            $tile_url = str_replace('y_value',$y,$tile_url);
            $tile_url = str_replace('z_value',$z,$tile_url);
            $str = 'wget -O '.$y_file.' "'.$tile_url.'"';
            //echo $str."\n";
            exec($str);
        }
        sleep(2);
    }
}

function getXTile($lon, $zoom) {
    return floor((($lon + 180) / 360) * pow(2, $zoom));   
}

function getYTile ($lat, $zoom) {
    return floor((1 - log(tan(deg2rad($lat)) + 1 / cos(deg2rad($lat))) / pi()) /2 * pow(2, $zoom));
}