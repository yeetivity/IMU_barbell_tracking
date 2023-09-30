
// Variables for Kalman filter
var xAccEstimate = 0;
var xAccEstimateError = 1;
var processVariance = 0.1; // You may need to fine-tune this value.
var measurementVariance = 1.0; // You may need to fine-tune this value.

// Variables for 1A
var oldXAcc = 0;
var maxSpeed = 0;
var maxAcc = 0;
var oldAcc = 0;
var filteredAcc = 0;
var speed = 0;
var oldspeed = 0;
var nmbrOfReps = 0;
var NumberOfSamples = 0;
var filteredAccX = 0;
var filteredAccY = 0;
var filteredAccZ = 0;
var accTot = 0;
var oldAccX = 0;
var oldAccY = 0;
var oldAccZ = 0;
var speedX = 0;
var speedY = 0;
var speedZ = 0;
var deltaVx = 0;
var deltaVy = 0;
var deltaVz = 0;

var ZangleFilter = 0;
var ZangleStart = 0;
var Zangle = 0;

var xGyroNew =0;
var yGyroNew =0;
var zGyroNew =0;

// array for storing values of acceleration
var accvalues = []
var speedvaluesXYZ = []
var speedvalues = []

const dT = 1/52;

var g = [0, -9.82, 0];

function filter(accDataPoint, gyroDataPoint) {

  // The sampling time is set under the function findPeriodCharacteristic to 52Hz

  // Raw data from sensor
  let xAccNew = accDataPoint.data.x;
  let yAccNew = accDataPoint.data.y;
  let zAccNew = accDataPoint.data.z;
  let xGyroNew = gyroDataPoint.data.x;
  let yGyroNew = gyroDataPoint.data.y;
  let zGyroNew = gyroDataPoint.data.z; //we have rotation aroung this axis in the barbell case

  //puts the values into a struct for array storage
  let accelerationdata = {
      x: xAccNew,
      y: yAccNew,
      z: zAccNew
  };

  // Prediction step
  const predictionError = xAccEstimateError + processVariance;

  // Update step
  const kalmanGain = predictionError / (predictionError + measurementVariance);
  xAccEstimate = xAccEstimate + kalmanGain * (xAccNew - xAccEstimate);
  xAccEstimateError = (1 - kalmanGain) * predictionError;

  console.log("xAccEstimate="+xAccEstimate)
  console.log("xAccEstimateError="+xAccEstimateError)

  deltaVx = 0.5*(xAccEstimate+oldAcc)*dT
  oldAccX = xAccEstimate;
  speedX += deltaVx
  if (xAccEstimate < 0.01) {
    speedX = 0
  }

  //calculates the total acceleration of the device

  let alpha = 0.2
  
  filteredAccX = alpha * filteredAccX + (1 - alpha) * xAccNew;
  filteredAccY = alpha * filteredAccY + (1 - alpha) * yAccNew;
  filteredAccZ = alpha * filteredAccZ + (1 - alpha) * zAccNew;

  //calculates start angle from function defined below
  getStartAngle();

  //should add small angle changes to the start angle
  Zangle = dT*zGyroNew+ZangleStart;
  
  // adds the values to the last element of the array
  accvalues.push(accelerationdata)

  //ZangleFilter = alpha * ZangleFilter + (1 - alpha) * Zangle;
  //console.log(Zangle)
  //console.log(checkMovement())


  //checkspeed();

  //stores the values from checkspeed to x,y and z direction. Stores every velocity change from each sample (52Hz)
  let velocitydata = {
    x: deltaVx,
    y: deltaVy,
    z: deltaVz
  }
  
  speedvalues.push(Math.abs(speed))
  plotOnRedLine(speedX*100)
  speedvaluesXYZ.push(velocitydata)

  //increases by one for every sample of the imu sensor
  NumberOfSamples++
}

//calculate all the neccesary speeds of the device
function checkspeed() {
  if (!checkMovement) {
    //small velocity changes in x direction
    deltaVx = 0.5*(filteredAccX+oldAccX)*dT
    oldAccX = filteredAccX;
    speedX += deltaVx
    
    //small velocity changes in y direction
    deltaVy = 0.5*(filteredAccY+oldAccY)*dT
    oldAccY = filteredAccY;
    speedY += deltaVy

    //small velocity changes in z direction
    deltaVz = 0.5*(filteredAccZ+oldAccZ)*dT
    oldAccZ = filteredAccZ;
    speedZ += deltaVz

    //calculates the total speed of the device
    speed += Math.sqrt(Math.pow(deltaVx,2)+Math.pow(deltaVy,2)+Math.pow(deltaVz,2))

  } else {
    //if the device is still reset the velocities
    speedX = 0
    speedY = 0
    speedZ = 0
    speed = 0
  }
}

function getStartAngle() {
  
  if(NumberOfSamples<=52) {
    ZangleStart += Math.acos(filteredAccY/-9.82) 
  } else if(NumberOfSamples == 53) {
    ZangleStart = ZangleStart/52
    console.log("angle= "+ZangleStart*(180/Math.PI))
  }
}

//function for checking if the sensor is moving
function checkMovement() {

  //Approxiamte threshold value to elmininate noise. 
  let thresholdacc = 1
  let thresholdgyro = 1

  //Checks if the absolute value is less than the trehsold to determine if still
  console.log("x:"+filteredAccX, "y:"+filteredAccY, "z:"+filteredAccZ)
  
  if(Math.abs(filteredAccX) <= thresholdacc && Math.abs(filteredAccY) <= thresholdacc && Math.abs(filteredAccZ-g) <= thresholdacc
   && Math.abs(xGyroNew) <= thresholdgyro && Math.abs(yGyroNew) <= thresholdgyro && Math.abs(zGyroNew) <= thresholdgyro) {
    return true;
  } else {
    return false;
  }
}

function saveVelocity() {

  // Convert velvalues array to JSON
  let velJson = JSON.stringify(speedvalues);

  // Create a Blob containing the JSON data
  let blob = new Blob([velJson], {type: "application/json"});

  // Construct the filename
  let filename = "vel.json";

  // Create an anchor element and click to trigger download
  let a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();

  console.log("saved");
}

function savexyzVelValues() {
    
    let xVel = [];
    let yVel = [];
    let zVel = [];

  for(let i = 0; i < speedvaluesXYZ.length; i++) {
    xVel.push(speedvaluesXYZ[i].x);
    yVel.push(speedvaluesXYZ[i].y);
    zVel.push(speedvaluesXYZ[i].z);
  }

  let velJson3 = {
    xVel: xVel,
    yVel: yVel, 
    zVel: zVel
  };

  // Convert accvalues array to JSON
  let velJson = JSON.stringify(velJson3);

  // Create a Blob containing the JSON data
  let blob = new Blob([velJson], {type: "application/json"});

  // Construct the filename
  let filename = "velxyz.json";

  // Create an anchor element and click to trigger download
  let a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();

  console.log("saved");

}


function saveAccValues() {

  let accX = [];
  let accY = []; 
  let accZ = [];

  for(let i = 0; i < accvalues.length; i++) {
    accX.push(accvalues[i].x);
    accY.push(accvalues[i].y);
    accZ.push(accvalues[i].z);
  }

  let accJson2 = {
    accX: accX,
    accY: accY, 
    accZ: accZ
  };

  // Convert accvalues array to JSON
  let accJson = JSON.stringify(accJson2);

  // Create a Blob containing the JSON data
  let blob = new Blob([accJson], {type: "application/json"});

  // Construct the filename
  let filename = "acc.json";

  // Create an anchor element and click to trigger download
  let a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();

  console.log("saved");

}