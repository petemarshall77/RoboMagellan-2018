// Cone detection using largest blob


import processing.video.*;
import processing.net.*;

Capture cam;
int last_frame_time;
color trackColor = color(255, 125, 25);
color nextColor = trackColor;
color black = color(255,255,255);
int threshold = 50;
ArrayList<Integer> current_blob;
ArrayList<Integer> biggest_blob;
int chunksize = 10;
color[] bloxels;
Server myserver;

void setup() {
  // Get the list of camera modes
  String[] cameras = Capture.list();
  for (int i = 0; i < cameras.length; i++) {
    println(i, cameras[i]);
  }
  cam = new Capture(this, cameras[30]);
  cam.start();
  
  // Screen settings
  size(640, 480);
  textSize(12);
  fill(255);
  
  // Start the network server
  myserver = new Server(this, 9788);
  
  // Get the saved trackcolor
  String[] savedColors = loadStrings("Colorsave.txt");
  nextColor = color(unbinary(savedColors[0]), unbinary(savedColors[1]), unbinary(savedColors[2]));
  
  current_blob = new ArrayList<Integer>();
  biggest_blob = new ArrayList<Integer>();

  bloxels = new color[(width*height)/(chunksize*chunksize)];
  last_frame_time = millis();
}


void draw()
{  
  // Handle the next available frame
  if (cam.available() == true) {
    cam.read();
    image(cam, 0, 0);
    loadPixels();
    blurFrame();
    processFrame();
    //updatePixels();    
  
    // Write the framerate
    float frame_rate = 1000.0/(millis() - last_frame_time);
    last_frame_time = millis();
    text("Framerate: " + str(frame_rate), 3, 12);
    
    // Update the track color
    trackColor = nextColor;
  }
  delay(50);
}

void blurFrame()
{
  int bloxelcounter = 0;
  for (int i = 0; i < width * height; i += width * chunksize)
  {
    for (int p = 0; p < width; p += chunksize)
    {
      int corner = i + p;
      int redsum = 0, greensum = 0, bluesum = 0;
      for(int y = 0; y < chunksize; y++)
      {
        for(int x = 0; x < chunksize; x++)
        {
          int loc = corner + x + (y * width);
          redsum += red(pixels[loc]);
          greensum += green(pixels[loc]);
          bluesum += blue(pixels[loc]);
          
        }
      }
      redsum /= (chunksize * chunksize);
      greensum /= (chunksize * chunksize);
      bluesum /= (chunksize * chunksize);
      for(int y = 0; y < chunksize; y++)
      {
        for(int x = 0; x < chunksize; x++)
        {
          int loc = corner + x + (y * width);
          pixels[loc] = color((int)redsum, (int)greensum, (int)bluesum);
        }
      }
      bloxels[bloxelcounter] = color((int)redsum, (int)greensum, (int)bluesum);
      bloxelcounter++;
    }
  }
  updatePixels();
}

void processFrame()
{
  biggest_blob.clear();
  for (int i = 0; i < ((width*height)/(chunksize*chunksize)); i++) {
    if (bloxels[i] != black && isColor(i) == true) {
      processBlob(i);
    }
  }
  updatePixels();
  println(biggest_blob.size());
  // Color the biggest blob
  for (int j = 0; j < biggest_blob.size(); j++) {
    paintBloxel(biggest_blob.get(j),color(0,255,0));
  }
  updatePixels();
  makeBox();
}


void processBlob(int loc)
{
  current_blob.clear();
  current_blob.add(loc);  // add our starting pixel to the blob
  int start_index = 0;
  
  // Go through the list of pixels, adding further pixels
  // to the list itself until no more pixels are found.
  while (true) {
    ArrayList<Integer> neighbors = new ArrayList<Integer>();
    neighbors = get_neighbors(current_blob.get(start_index));
    for (int i = 0; i < neighbors.size(); i++) { 
      //if (inCurrentBlob(neighbors.get(i)) == false) { // Don't add to list if it already exists.
      if (!current_blob.contains(neighbors.get(i))) {
        current_blob.add(neighbors.get(i));
        paintBloxel(neighbors.get(i), black);
        bloxels[neighbors.get(i)] = black;
      } //<>//
    }
    start_index += 1;
    if (start_index >= current_blob.size()) {
      break;
    }
  }
  
  // Is this the new biggest blob?
  if (current_blob.size() > biggest_blob.size()) {
    biggest_blob.clear();
    for(int i = 0; i < current_blob.size(); i++)
    {
      biggest_blob.add(current_blob.get(i));
    }
    //println(biggest_blob.size());
  }
}

ArrayList get_neighbors(int loc) {
  ArrayList<Integer> neighbors = new ArrayList<Integer>();
  int target;
  
  target = loc + 1;
  if(target % (width/chunksize) != 0){
   if(isColor(target) == true){
     neighbors.add(target);
    }
  }
  
  target = loc + (width/chunksize) - 1;
  if(loc % (width/chunksize) != 0){
    if(target < (width/chunksize)*(height/chunksize)){
      if(isColor(target) == true){
       neighbors.add(target); 
      }
    }
  }
  
  target = loc + (width/chunksize);
  if(target < (width/chunksize)*(height/chunksize)){
    if(isColor(target) == true){
      neighbors.add(target);
    }
  }
  
  target = loc + (width/chunksize) + 1;
  if(target < (width/chunksize) * (height/chunksize)){
    if(target % (width/chunksize) != 0){
      if(isColor(target)){
        neighbors.add(target);
      }
    }
  }
  
  target = loc - (width/chunksize) - 1;
  if(target > ((width/chunksize) - 1)){
    if(loc % (width/chunksize) != 0){
      if(isColor(target)){
        neighbors.add(target);
      }
    }
  }
  
  return neighbors;
}


boolean inCurrentBlob(int val)
{
  for (int i = 0; i < current_blob.size(); i++) {
    if (current_blob.get(i) == val) {
      return true;
    }
  }
  return false;
}

boolean isColor(int loc)
{
  color cc = bloxels[loc]; // current color
  color tc = trackColor;  // track color
  
  if (dist(red(cc), green(cc), blue(cc), red(tc), green(tc), blue(tc)) < threshold) {
    return true;
  } else {
    return false;
  }
}

void paintBloxel(int bloxnum, color paint)
{
  int startx = ((bloxnum % (width/chunksize)) * chunksize);
  int starty = (int)(bloxnum/(width/chunksize)) * chunksize;
  for(int y = 0; y < chunksize; y++)
  {
    for(int x = 0; x < chunksize; x++)
    {
      pixels[startx + (starty * width) + x + (y * width)] = paint;
    }
  }
}

void makeBox()
{
  if (biggest_blob.size() == 0)
  {
    return;
  }
  int topMost = height/chunksize + 1;
  int bottomMost = 0;
  int leftMost = width/chunksize + 1;
  int rightMost = 0;
  int xCoord = 0;
  int yCoord = 0;
  int xSum = 0;
  int ySum = 0;
  int xAvg = 0;
  int yAvg = 0;
  
  for (int i = 0; i < biggest_blob.size(); i++)
  {
    xCoord = biggest_blob.get(i) % (width/chunksize);
    yCoord = (int)(biggest_blob.get(i) / (width/chunksize));
    
    if(yCoord < topMost)
    {
      topMost = yCoord;
    }
    if(yCoord > bottomMost)
    {
      bottomMost = yCoord;
    }
    if(xCoord < leftMost)
    {
      leftMost = xCoord;
    }
    if(xCoord > rightMost)
    {
      rightMost = xCoord;
    }
    
    xSum += xCoord;
    ySum += yCoord;
  }
  xAvg = xSum / biggest_blob.size();
  yAvg = ySum / biggest_blob.size();
  
  strokeWeight(5.0);
  stroke(0, 0, 255);
  noFill();
  //fill(0,0,255);
  rect((leftMost*chunksize), (topMost*chunksize), ((rightMost-leftMost)*chunksize + chunksize), ((bottomMost-topMost)*chunksize) + chunksize);
  
  line(xAvg*chunksize, topMost*chunksize, xAvg*chunksize, bottomMost*chunksize+chunksize);
  line(leftMost*chunksize, yAvg*chunksize, rightMost*chunksize+chunksize, yAvg*chunksize);

  // Write data to network
  myserver.write(xAvg + "," + biggest_blob.size());
}

void mousePressed() { //<>//
  // Save color where the mouse is clicked in trackColor variable
  int loc = mouseX + mouseY*width;
  nextColor = pixels[loc];
  String[] saveString = {binary((int)red(nextColor)), binary((int)green(nextColor)), binary((int)blue(nextColor))};
  println(saveString);
  saveStrings("Colorsave.txt", saveString);
}