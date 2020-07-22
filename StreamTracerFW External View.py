from paraview.simple import *
import numpy
renderView1 = GetActiveView()
paraview.simple._DisableFirstRenderCameraReset()

############# DA COMPLETARE - INIZIO #####################
#Posizione File
png_output_directory = "D:\\Dynamis\\Script\\FotoScript\\Esterne\\"
casefoam = OpenFOAMReader(FileName='D:\\Dynamis\\CFD\\DPX\\case.foam')

# create a new 'Legacy VTK Reader'
legacyVTKReader1 = LegacyVTKReader(FileNames=['D:\\Dynamis\\CFD\\DPX\\VTK\\DPX_800.vtk'])
#Impostazioni ScreenShot
trasp = 0 #mettere 1 per sfondo trasparente, 0 altrimenti

#Camere
posizione = numpy.matrix([[0.5, -4.7, 0.5], [-3, 0.02, 0.5], [-3.6, -2.5, 2.9], [0.41, -0.04, -4.37], [4.5, 0, 0.6], [0.8, -0.05, 5.5]]) #per ogni riga una posizione
focal = numpy.matrix([[0.5, 6, 0.5], [4, 0.02, 0.5], [1.6, 0.83, -0.42], [0.41, -0.04, 2.57], [-2.5, 0, 0.6], [0.8, -0.05, -1.42]])
angolazione = numpy.matrix([[0, 0, 1], [0, 0, 1], [0.46, 0.17, 0.87], [0, -1, 0], [0, 0, 1], [0, 1, 0]]) #per ogni riga una angolazione

#Campi
Campi = ['p', 'U']
range_val = numpy.matrix([[-150, 150], [0, 32]])
############# DA COMPLETARE - FINE #####################

## Apertura file
casefoam.MeshRegions = ['DPX_FW', 'DPX_RW', 'DPX_SP', 'DPX_Monocoque', 'ground', 'DPX_RWheels', 'DPX_FWheels']
SetActiveSource(casefoam)
reader = GetActiveSource()
tsteps = reader.TimestepValues
renderView1.ViewTime = tsteps[-1]

# create a new 'Reflect'
reflect1 = Reflect(Input=casefoam)
reflect1.Plane = 'Y Min'
reflect1Display = Show(reflect1, renderView1)

#Gestione LUT
LUT = GetColorTransferFunction("br")
opacityLUT = GetOpacityTransferFunction("br")

# create a new 'Stream Tracer'
streamTracer1 = StreamTracer(Input=legacyVTKReader1, SeedType='High Resolution Line Source')
streamTracer1.Vectors = ['POINTS', 'U']
streamTracer1.MaximumStreamlineLength = 8.0

# init the 'High Resolution Line Source' selected for 'SeedType'
streamTracer1.SeedType.Point1 = [-2.0, 0.1, 0.08]
streamTracer1.SeedType.Point2 = [-2.0, 0.8, 0.08]
streamTracer1.SeedType.Resolution = 50
streamTracer1.IntegrationDirection = 'FORWARD'
streamTracer1Display = Show(streamTracer1, renderView1)

# show data from streamTracer1
streamTracer1Display = Show(streamTracer1, renderView1)

numero_Camere = len(posizione)

# trace defaults for the display properties.
streamTracer1Display.Representation = 'Surface'
streamTracer1Display.ColorArrayName = ['POINTS', 'U']
streamTracer1Display.LookupTable = LUT

for i in range(numero_Camere):
	for j in range(len(Campi)):
		renderView1.CameraPosition = [posizione[i, 0], posizione[i, 1], posizione[i, 2]]
		renderView1.CameraFocalPoint = [focal[i, 0], focal[i, 1], focal[i, 2]]
		renderView1.CameraViewUp = [angolazione[i, 0], angolazione[i, 1], angolazione[i, 2]]
		
		#Scala
		LUT = GetColorTransferFunction("br")
		opacityLUT = GetOpacityTransferFunction("br")
		LUT.RescaleTransferFunction(range_val[j, 0], range_val[j, 1])
		#Riscalatura
		opacityLUT.RescaleTransferFunction(range_val[j, 0], range_val[j, 1])
		LUT.AutomaticRescaleRangeMode = 'Never'
		LUT.ScalarRangeInitialized = 1.0
		LUTColorBar = GetScalarBar(LUT, renderView1)
		LUTColorBar.Title = Campi[j]
		LUTColorBar.Visibility = 1
		reflect1Display.Representation = 'Surface'
		reflect1Display.ColorArrayName = ['POINTS', Campi[j]]
		reflect1Display.LookupTable = LUT
		reflect1Display.SetScalarBarVisibility(renderView1, True)
		
		#ScreenShot
		out_filename = "Screen_" + Campi[j] + "_" + str(i) + ".png"
		writefile = png_output_directory + out_filename
		paraview.simple.SaveScreenshot(writefile, renderView1, ImageResolution=[1920, 1080], TransparentBackground=trasp, CompressionLevel=0)
		LUTColorBar.Visibility = 0