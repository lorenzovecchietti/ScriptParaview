from paraview.simple import *
import numpy
renderView1 = GetActiveView()
renderView1.ViewSize = [1920, 1080]
paraview.simple._DisableFirstRenderCameraReset()
LoadDistributedPlugin("SurfaceLIC", remote=False, ns=globals())

############# DA COMPLETARE - INIZIO #####################
#Posizione File
png_output_directory = "D:\\Dynamis\\Script\\FotoScript\\Z\\"
casefoam = OpenFOAMReader(FileName='D:\\Dynamis\\CFD\\DPX\\case.foam')

#Posizione Camera
renderView1.CameraPosition = [1.9, -0.4, 261]
renderView1.CameraFocalPoint =[1.9, -0.4, 25]
renderView1.CameraViewUp = [0, 1, 0]
renderView1.InteractionMode = '2D'

trasp = 0 #mettere 1 per sfondo trasparente, 0 altrimenti

# Posizione e tipo di Slice
z_pt = numpy.around(numpy.arange(0, 1.5, 0.05), decimals=2)
y_pt = numpy.zeros((len(z_pt)))
x_pt = numpy.zeros((len(z_pt)))

z_normal = numpy.ones((len(z_pt)))
y_normal = numpy.zeros((len(z_pt)))
x_normal = numpy.zeros((len(z_pt)))
campi = ['p', 'U']
scala = numpy.matrix([[-150, 150], [0, 32]])
############# DA COMPLETARE - FINE #####################


## Apertura file
casefoam.MeshRegions = ['internalMesh']
SetActiveSource(casefoam)
reader = GetActiveSource()
tsteps = reader.TimestepValues
renderView1.ViewTime = tsteps[-1]

## Crea'Slice'
slice1 = Slice(Input=casefoam)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]
slice1Display = Show(slice1, renderView1)

for i in range(len(z_pt)):
	slice1.SliceType.Origin = [x_pt[i], y_pt[i], z_pt[i]]
	slice1.SliceType.Normal = [x_normal[i], y_normal[i], z_normal[i]]
	for j in range(len(campi)):
		slice1Display.Representation = 'Surface'
		slice1Display.ColorArrayName = ['POINTS', campi[j]]
		# get color transfer function/color map for 'br'
		pLUT = GetColorTransferFunction("br")
		opacitypLUT = GetOpacityTransferFunction("br")
		# Rescale transfer function
		pLUT.RescaleTransferFunction(scala[j, 0], scala[j, 1])
		opacitypLUT.RescaleTransferFunction(scala[j, 0], scala[j, 1])
		pLUT.AutomaticRescaleRangeMode = 'Never'
		pLUT.ScalarRangeInitialized = 1.0
		slice1Display.LookupTable = pLUT
		# get color legend/bar for pLUT in view renderView1
		pLUTColorBar = GetScalarBar(pLUT, renderView1)
		pLUTColorBar.Title = campi[j]
		pLUTColorBar.Visibility = 1
		pLUTColorBar.Orientation = 'Horizontal'
		pLUTColorBar.Position = [0.37, 0.1]
		# show color legend
		slice1Display.SetScalarBarVisibility(renderView1, True)
		SetActiveSource(casefoam)
		Render()
		stringnorm = "_" + str(i) + "_z_" + str(z_pt[i])
		out_filename = campi[j] + stringnorm + ".png"
		writefile = png_output_directory + out_filename
		paraview.simple.SaveScreenshot(writefile, renderView1, ImageResolution=[1920, 1080], TransparentBackground=trasp, CompressionLevel=5)
		if campi[j]=='U':
			slice1Display.Representation = 'Surface LIC'
			slice1Display.ColorMode = 'Multiply'
			slice1Display.LICIntensity = 0.7
			slice1Display.EnhanceContrast = 'Color Only'
			out_filename = 'LIC' + stringnorm + ".png"
			writefile = png_output_directory + out_filename
			paraview.simple.SaveScreenshot(writefile, renderView1, ImageResolution=[1920, 1080], TransparentBackground=trasp, CompressionLevel=5)
		pLUTColorBar.Visibility = 0