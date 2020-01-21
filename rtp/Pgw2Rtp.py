import gi
import sys
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib
import enum
from abc import ABCMeta, abstractmethod


class GObjectRtp(metaclass=ABCMeta):
    class State(enum.Enum):
        _INIT = 0
        _READY = 1
        _START = 2
        _PAUSE = 3
        _STOP = 4

    def __init__(self):
        self.state = self.State._INIT
        # GObject.threads_init()
        Gst.init()

        # the pipeline to hold everything
        self.pipeline = Gst.Pipeline.new()

    @abstractmethod
    def InitGObjectRtp(self, host, port):
        self.state = self.State._READY
        pass

    def StartRtp(self):
        if self.state not in [self.State._READY, self.State._PAUSE]:
            return
        self.state = self.State._START
        Gst.Element.set_state(self.pipeline, Gst.State.PLAYING)

    def PauseRtp(self):
        if self.state not in [self.State._START]:
            return
        self.state = self.State._PAUSE
        super().PauseRtp()
        Gst.Element.set_state(self.pipeline, Gst.State.NULL)

    def StopRtp(self):
        if self.state not in [self.State._READY, self.State._START, self.State._PAUSE]:
            return
        self.state = self.State._STOP
        Gst.Element.set_state(self.pipeline, Gst.State.NULL)
        Gst.Object.unref(self.pipeline)


class RtpSender(GObjectRtp):
    def InitGObjectRtp(self, host, port):
        super().InitGObjectRtp(host, port)
        # filesrc location="opus_48000KHz_2Channel_20kBitrate.opus" 

        # spec = """
        # filesrc location="PCMU_60sec.wav" 
        # ! decodebin 
        # ! audioconvert 
        # ! opusenc bitrate=32000
        # ! rtpopuspay pt=96
        # ! queue 
        # ! udpsink host={0}  port={1}
        # """.format(host, port)

        # "audio/x-raw, rate=12000"

        #         spec = """
        # filesrc location="PCMU_60sec.wav" 
        # ! decodebin 
        # ! audioconvert 
        # ! opus.sink \
        #     opusenc name=opus bitrate=32000 \
        #   opus.src \
        # ! rtpopuspay pt=96
        # ! queue 
        # ! udpsink host={0}  port={1}
        # """.format(host, port)

        others = """
        uridecodebin uri=file:///home/ysh8361/workspace/sim_pgw2/PCMU_60sec.wav 
        ! audioconvert 
        ! audioresample 
        ! audio/x-raw, rate=8000 
        ! autoaudiosink
        """

        # spec = """
        # filesrc location="PCMU_60sec.wav" 
        # ! decodebin 
        # ! audioconvert 
        # ! audioresample 
        # ! audio/x-raw, rate=16000, channels=1, format=S16LE
        # ! opus.sink \
        #     opusenc name=opus \
        #   opus.src \
        # ! rtpopuspay pt=96
        # ! queue 
        # ! udpsink host={0}  port={1}
        # """.format(host, port)
        spec = """
        filesrc location="PCMU_60sec.wav" 
        ! decodebin 
        ! audioconvert 
        ! audioresample 
        ! audio/x-raw, rate=16000, channels=1, format=S16LE
        ! opus.sink \
            opusenc name=opus \
          opus.src \
        ! oggmux
        ! filesink location=test.ogg
        """.format(host, port)

        self.pipeline = Gst.parse_launch(spec)

        #GST_DEBUG=3 gst-launch-1.0 filesrc location="PCMU_60sec.wav" ! decodebin !  audioconvert ! rtpL16pay ! queue ! udpsink host=192.168.0.192  port=5002
        # src = Gst.ElementFactory.make('filesrc', 'src')
        # src.set_property('location', '/home/ysh8361/workspace/sim_pgw2/PCMU_60sec.wav')
        # decode = Gst.ElementFactory.make('decodebin', 'decode')
        # audioconv = Gst.ElementFactory.make('audioconvert', 'audioconv')
        # rtppay = Gst.ElementFactory.make('rtpL16pay', 'rtppay')
        # # add capture and payloading to the pipeline and link
        # self.pipeline.add(src)
        # self.pipeline.add(decode)
        # self.pipeline.add(audioconv)
        # self.pipeline.add(rtppay)

        # src.link(decode)
        # decode.link(audioconv)
        # audioconv.link(rtppay)

        # # the rtpbin element
        # rtpbin = Gst.ElementFactory.make('rtpbin', 'rtpbin')

        # self.pipeline.add(rtpbin)

        # # # the udp sinks and source we will use for RTP and RTCP
        # rtpsink = Gst.ElementFactory.make('udpsink', 'rtpsink')
        # rtpsink.set_property('port', port)
        # rtpsink.set_property('host', host)

        # self.pipeline.add(rtpsink)

        # # now link all to the rtpbin, start by getting an RTP sinkpad for session 0
        # sinkpad = Gst.Element.get_request_pad(rtpbin, 'send_rtp_sink_0')
        # srcpad = Gst.Element.get_static_pad(rtppay, 'src')
        # lres = Gst.Pad.link(srcpad, sinkpad)

        # # get the RTP srcpad that was created when we requested the sinkpad above and
        # # link it to the rtpsink sinkpad
        # srcpad = Gst.Element.get_static_pad(rtpbin, 'send_rtp_src_0')
        # sinkpad = Gst.Element.get_static_pad(rtpsink, 'sink')
        # lres = Gst.Pad.link(srcpad, sinkpad)


class RtpReceiver(GObjectRtp):
    #       gst-launch -v rtpbin name=rtpbin                                                \
    #       udpsrc caps='application/x-rtp,media=(string)audio,clock-rate=(int)8000,encoding-name=(string)PCMA' port=$RTP_RECV_PORT ! rtpbin.recv_rtp_sink_0              \
    #             rtpbin. ! rtppcmadepay ! alawdec ! audioconvert ! audioresample ! autoaudiosink \
    #           udpsrc port=$RTCP_RECV_PORT ! rtpbin.recv_rtcp_sink_0                              \
    #         rtpbin.send_rtcp_src_0 ! udpsink port=$RTCP_SEND_PORT host=$DEST sync=false async=false
    def InitGObjectRtp(self, host, port):
        super().InitGObjectRtp(host, port)

        def pad_added_cb(rtpbin, new_pad, depay):
            sinkpad = Gst.Element.get_static_pad(depay, 'sink')
            lres = Gst.Pad.link(new_pad, sinkpad)

        # the udp src and source we will use for RTP and RTCP
        rtpsrc = Gst.ElementFactory.make('udpsrc', 'rtpsrc')
        rtpsrc.set_property('port', port)

        # we need to set caps on the udpsrc for the RTP data
        caps = Gst.caps_from_string('application/x-rtp,media=(string)audio,clock-rate=(int)48000,encoding-name=(string)OPUS')
        rtpsrc.set_property('caps', caps)

        self.pipeline.add(rtpsrc)

        # the depayloading and decoding
        audiodepay = Gst.ElementFactory.make('rtpopusdepay', 'audiodepay')
        audiodec = Gst.ElementFactory.make('opusdec', 'audiodec')

        # the audio playback and format conversion
        audioconv = Gst.ElementFactory.make('audioconvert', 'audioconv')
        audiores = Gst.ElementFactory.make('audioresample', 'audiores')
        audiosink = Gst.ElementFactory.make('autoaudiosink', 'audiosink')

        # add depayloading and playback to the pipeline and link
        self.pipeline.add(audiodepay)
        self.pipeline.add(audiodec)
        self.pipeline.add(audioconv)
        self.pipeline.add(audiores)
        self.pipeline.add(audiosink)

        audiodepay.link(audiodec)
        audiodec.link(audioconv)
        audioconv.link(audiores)
        audiores.link(audiosink)

        # the rtpbin element
        rtpbin = Gst.ElementFactory.make('rtpbin', 'rtpbin')        

        self.pipeline.add(rtpbin)

        # now link all to the rtpbin, start by getting an RTP sinkpad for session 0
        srcpad = Gst.Element.get_static_pad(rtpsrc, 'src')
        sinkpad = Gst.Element.get_request_pad(rtpbin, 'recv_rtp_sink_0')
        lres = Gst.Pad.link(srcpad, sinkpad)

        rtpbin.connect('pad-added', pad_added_cb, audiodepay)


def main():
    print('start')
    rtpSender = RtpSender()
    rtpSender.InitGObjectRtp('192.168.0.207', 5002)
    rtpSender.StartRtp()

    rtpReceiver = RtpReceiver()
    rtpReceiver.InitGObjectRtp('0.0.0.0', 5002)
    rtpReceiver.StartRtp()
    print('loop start')
    mainloop = GLib.MainLoop()
    mainloop.run()
    print('loop end')


if __name__ == '__main__':
    main()
