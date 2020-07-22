from paraview.simple import *
import numpy
renderView1 = GetActiveView()
renderView1.ViewSize = [1920, 1080]

############# DA COMPLETARE - INIZIO #####################
#Posizione File
png_output_directory = "D:\\Dynamis\\Script\\FotoScript\\CPRWGraph\\"
casefoam = OpenFOAMReader(FileName='D:\\Dynamis\\CFD\\DPX\\case.foam')

#Posizione Camera
renderView1.CenterOfRotation = [1.5, -0.2, 0.75]
renderView1.CameraPosition = [1.5, -3, 0.9]
renderView1.CameraFocalPoint = [1.5, -0.2, 0.9]
renderView1.CameraViewUp = [0, 0, 1]
renderView1.InteractionMode = '2D'
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.OrientationAxesVisibility = 0


trasp = 0 #mettere 1 per sfondo trasparente, 0 altrimenti

# Posizione e tipo di Slice
y_pt = numpy.around(numpy.arange(-0.46, 0, 0.02), decimals=2)
x_pt = numpy.zeros((len(y_pt)))
z_pt = numpy.zeros((len(y_pt)))

x_normal = numpy.zeros((len(y_pt)))
y_normal = numpy.ones((len(y_pt)))
z_normal = numpy.zeros((len(y_pt)))
campi = ['p']
scala = numpy.matrix([[-150, 150], [0, 32]])
############# DA COMPLETARE - FINE #####################


## Apertura file
casefoam.MeshRegions = ['internalMesh', 'solid_0_RW']
casefoam.CellArrays = ['p']
SetActiveSource(casefoam)
reader = GetActiveSource()
tsteps = reader.TimestepValues
renderView1.ViewTime = tsteps[-1]

extractBlock1 = ExtractBlock(Input=casefoam)
extractBlock1.BlockIndices = [2]

# create a new 'Warp By Scalar'
warpByScalar1 = WarpByScalar(Input=extractBlock1)
warpByScalar1.ScaleFactor = 0.0005

# create a new 'Slice'
slice2 = Slice(Input=warpByScalar1)
slice2.SliceType = 'Plane'
slice2.SliceOffsetValues = [0.0]
slice2Display = Show(slice2, renderView1)
slice2Display.ColorArrayName = ['POINTS', 'p']
# init the 'Plane' selected for 'SliceType'

slice2.SliceType.Normal = [0.0, 1.0, 0.0]

# create a new 'Slice'
slice1 = Slice(Input=extractBlock1)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]
slice1Display = Show(slice1, renderView1)

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

renderView1.Background = [0.1, 0.1, 0.1]

for i in range(len(x_pt)):
    slice1.SliceType.Origin = [x_pt[i], y_pt[i], z_pt[i]]
    slice1.SliceType.Normal = [x_normal[i], y_normal[i], z_normal[i]]
    slice2.SliceType.Origin = [x_pt[i], y_pt[i], z_pt[i]]
    for j in range(len(campi)):
        warpByScalar1.Scalars = ['POINTS', 'p']
        slice1Display.Representation = 'Surface'
        slice1Display.ColorArrayName = ['POINTS']
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
        stringnorm = str(i) + "_y_" + str(y_pt[i])
        out_filename = campi[j] + stringnorm + ".png"
        writefile = png_output_directory + out_filename
        paraview.simple.SaveScreenshot(writefile, renderView1, ImageResolution=[1920, 1080], TransparentBackground=trasp, CompressionLevel=5)
        pLUTColorBar.Visibility = 0