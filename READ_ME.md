# Pi Sense hat project.

A flask interface designed to allow images to be displayed on the sense hat's 8 x 8 display (via RGB values) remotely.  

* RGB data can be sent to the display in the following ways:  
  1. GET:  
  
  for a json file on local storage DIR 'patterns':  
  get-command/?set=jumble.json  
  
  directly sending the RGB values:  
  get-command/?set=[[255,255,255], [255,255,255], [255,255,255], .....] (len must be 64, no null values)

  2. POST:  
  
  UI PAGE: ui-command/  
  
  post-set-img/  
  This expects json data to sent to it in the same format as the local json files in the 'patterns' DIR  
  Example from cmd window:  
  import requests  
  json_data = {  
      "base": [100, 0, 60],  
      "red":  
      {  
          "130": [16],  
          "120": [3, 39, 21],  
          "100": [50, 35, 7],  
          "80": [38, 10, 2, 46]  
      },  
      "green":  
      {  
          "160": [55],  
          "150": [0, 7, 12],  
          "130": [15],  
          "120": [3, 42, 45],  
          "100": [22, 35, 36],  
          "80": [17, 18, 58, 61],  
          "60": [21, 25, 30],  
          "40": [26, 29, 43, 44, 50, 51, 52, 53]  
    }  
  }  
  r = requests.post("http://IP/post-set-img/", json=json_data)  
  
* Rotating the displayed image:  
  
  1. Example of a post cmd window, rotating an image already loaded onto the display:  

  import requests  
  json_data = {  
      "cmd": "simple",   
      "rotate_vals": [0, 90, 180, 270],   
      "re_draw": True,  
      "background": True  
    }  
  r = requests.post("http://IP/post_rotation/", json=json_data)  
  
  ending the rotation:  
  json_data = {"cmd": "kill"}  
  
* Fetching the loaded image's RGB values can be done by:  
  
  1. GET:  
    get-command/?get  
    it is returned when setting an image via get-command/  

  2. POST:  
    Current RGB values are always returned by post-set-img/  
    Using the above post-set-img example, 'r.text' would give you the RGB values.  
