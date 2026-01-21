import numpy as np
from qtpy.QtCore import QThread, Slot, QRectF
from qtpy import QtWidgets

from pymodaq_utils.utils import ThreadCommand
from pymodaq_data.data import DataToExport, Axis
from pymodaq_gui.parameter import Parameter

from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins

from pymodaq_plugins_mockexamples.daq_viewer_plugins.plugins_2D.daq_2Dviewer_BSCamera import DAQ_2DViewer_BSCamera

import laserbeamsize as lbs

class DAQ_2DViewer_BeamProfiler(DAQ_2DViewer_BSCamera):
    """ Instrument plugin class for a 2D viewer.

       Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """

    params = DAQ_2DViewer_BSCamera.params + [
        {'title': 'Beam', 'name': 'beam', 'type': 'bool_push', 'value': True},
        {'title': 'Position', 'name': 'position', 'type': 'bool_push', 'value': True},
        {'title': 'Size', 'name': 'bsize', 'type': 'bool_push', 'value': True},
        {'title': 'Angle', 'name': 'bangle', 'type': 'bool_push', 'value': True}
    ]



    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        data = self.average_data(Naverage)
        beam = data[0].data[0]

        x, y, d_major, d_minor, phi = lbs.beam_size(beam)

        dte = DataToExport('BeamProfiler',
                           data=[
                               DataFromPlugins('Beam',
                                               data=[beam],
                                               labels=['Row beam'],
                                               do_plot=self.settings['beam']),
                               DataFromPlugins('Position',
                                               data=[np.atleast_1d(x),
                                                     np.atleast_1d(y)],
                                               labels=['x', 'y'],
                                               do_plot=self.settings['position']),
                               DataFromPlugins('Size',
                                               data=[np.atleast_1d(d_major),
                                                     np.atleast_1d(d_minor)],
                                               labels=['Major', 'Minor'],
                                               do_plot=self.settings['bsize']),
                               DataFromPlugins('Angle',
                                               data=[np.atleast_1d(phi)],
                                               labels=['Angle'],
                                               do_plot=self.settings['bangle'])
                           ])

        self.dte_signal.emit(dte)

    if __name__ == '__main__':
        main(__file__)