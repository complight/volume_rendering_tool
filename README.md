# Volume-Rendering-Tool
This tool transforms image sequence data into 3D objects.

## Quickstart

### Install the required packages(1)

Basically `pip install requirements.txt`

Manually you can download via links:
[Python](https://www.python.org/downloads/)/
[Blender](https://www.blender.org/download/)/
[SpriteTool](https://github.com/TravisLedo/SpriteTool)

### Sprite Tool Preprocess(2)
Go to SpriteTool and make all images **side-by-side** 
![alt text](https://github.com/serhataksoy/Volume-Rendering-Tool/blob/main/Images/SpliteTool.JPG)

### Run code in blender(3)
Open blender and go to scripting area

Change Render method to **CYCLES**,you can write this in command line in blender `bpy.context.scene.render.engine = 'CYCLES'`

Click folder button and find **VolumeRenderingTool.py**.Then run it.

Go to Layout menu and you can see Volume Rendering Tool in right bar.

![alt text](https://github.com/serhataksoy/Volume-Rendering-Tool/blob/main/Images/VolumeRendering.JPG)

Select file,color and how many images did you use ,then select a cube in 3D Viewport menu and click ChangeMaterial.

### Reference(4)

This tool based on PGMath's [Stackoverflow](https://blender.stackexchange.com/questions/62110/using-image-sequence-of-medical-scans-as-volume-data-in-cycles) answer.




