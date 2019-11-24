#! /usr/bin/env python
from time import sleep
import gi
import sys
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

#gst-launch -v rtpbin name=rtpbin audiotestsrc ! audioconvert ! alawenc ! rtppcmapay ! rtpbin.send_rtp_sink_0 \
#                rtpbin.send_rtp_src_0 ! udpsink port=10000 host=xxx.xxx.xxx.xxx \
#                rtpbin.send_rtcp_src_0 ! udpsink port=10001 host=xxx.xxx.xxx.xxx sync=false async=false \
#                udpsrc port=10002 ! rtpbin.recv_rtcp_sink_0

class RTP:
    
    def SendRtp(self, to_ip, to_port):
        DEST_HOST = to_ip

        AUDIO_SRC = 'audiotestsrc'
        AUDIO_ENC = 'alawenc'
        AUDIO_PAY = 'rtppcmapay'

        RTP_SEND_PORT = to_port

        GObject.threads_init()
        Gst.init(sys.argv)

        # the pipeline to hold everything
        self.pipeline = Gst.Pipeline.new()

        # the pipeline to hold everything
        audiosrc = Gst.ElementFactory.make(AUDIO_SRC, 'audiosrc')
        audioconv = Gst.ElementFactory.make('audioconvert', 'audioconv')
        audiores = Gst.ElementFactory.make('audioresample', 'audiores')
        audioenc = Gst.ElementFactory.make(AUDIO_ENC, 'audioenc')
        audiopay = Gst.ElementFactory.make(AUDIO_PAY, 'audiopay')

        # add capture and payloading to the pipeline and link
        self.pipeline.add(audiosrc)
        self.pipeline.add(audioconv)
        self.pipeline.add(audiores)
        self.pipeline.add(audioenc)
        self.pipeline.add(audiopay)

        audiosrc.link(audioconv)
        audioconv.link(audiores)
        audiores.link(audioenc)
        audioenc.link(audiopay)

        # the rtpbin element
        rtpbin = Gst.ElementFactory.make('rtpbin', 'rtpbin')

        self.pipeline.add(rtpbin)

        # the udp sinks and source we will use for RTP and RTCP
        rtpsink = Gst.ElementFactory.make('udpsink', 'rtpsink')
        rtpsink.set_property('port', RTP_SEND_PORT)
        rtpsink.set_property('host', DEST_HOST)

        self.pipeline.add(rtpsink)

        # now link all to the rtpbin, start by getting an RTP sinkpad for session 0
        sinkpad = Gst.Element.get_request_pad(rtpbin, 'send_rtp_sink_0')
        srcpad = Gst.Element.get_static_pad(audiopay, 'src')
        lres = Gst.Pad.link(srcpad, sinkpad)

        # get the RTP srcpad that was created when we requested the sinkpad above and
        # link it to the rtpsink sinkpad
        srcpad = Gst.Element.get_static_pad(rtpbin, 'send_rtp_src_0')
        sinkpad = Gst.Element.get_static_pad(rtpsink, 'sink')
        lres = Gst.Pad.link(srcpad, sinkpad)

        # set the pipeline to playing
        Gst.Element.set_state(self.pipeline, Gst.State.PLAYING)

        # we need to run a GLib main loop to get the messages
        # mainloop = GObject.MainLoop()
        # mainloop.run()

    def StopRtp(self):

        Gst.Element.set_state(self.pipeline, Gst.State.NULL)
        Gst.Object.unref(self.pipeline)

    def RestartRtp(self):
        Gst.Element.set_state(self.pipeline, Gst.State.PLAYING)
        mainloop = GObject.MainLoop()
        mainloop.run()

rtp = RTP()
rtp.SendRtp('106.243.158.190', 5000)
sleep(10)
rtp.StopRtp()
sleep(5)
rtp.RestartRtp()


