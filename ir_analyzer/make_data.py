#returnする値をバラバラに分けたやつ
import numpy as np
import music21 as m21
import matplotlib.pyplot as plt

class Data():
    def getter(self, fn, part_num = 0):
        song = m21.converter.parse(fn)
        # process the ties
        song = song.stripTies()
        count = 0
        tone_list = []
        i = 0;
        for a in song:
            if a.isStream:
                e = m21.repeat.Expander(a)
                s2 = e.process()
                timing = s2.secondsMap
                song[i] = s2
            i += 1;
        
        for i, j in enumerate(song.parts):
            for a in j.recurse().notesAndRests:
                x = a;
                if (a.isNote):
                    tone = []
                    tone.append(x.pitch.ps)
                    tone.append(float(x.offset))
                    tone.append(float(x.quarterLength))
                    tone.append(x.beatStrength)
                    tone.append(x.measureNumber)
                    tone.append(count)
                    tone.append(i) ##パート
                    count += 1
                    tone_list.append(tone)
                elif(a.isChord):
                    for x in a._notes:
                        tone = []
                        tone.append(x.pitch.ps)
                        tone.append(float(a.offset))
                        tone.append(float(x.quarterLength))
                        tone.append(a.beatStrength)
                        tone.append(a.measureNumber)
                        tone.append(count)
                        tone.append(i) #パート
                        count += 1
                        tone_list.append(tone)
                elif(a.isRest):
                    tone = []
                    tone.append(-1)
                    tone.append(float(a.offset))
                    tone.append(float(x.quarterLength))
                    tone.append(a.beatStrength)
                    tone.append(a.measureNumber)
                    tone.append(count)
                    tone.append(i) #パート
                    count += 1
                    tone_list.append(tone)
                                   
        """
        #fn = sample2.music"3 Schubert-Pf-D946-No2_easy.musicxml"
        #fn = "tmp.musicxml"
        xml_data = m21.converter.parse(fn) #score_object
        xml_list = []

        for part_index, part in enumerate(xml_data.parts):
            if(part_index == part_num): #ここでパートを選択？
                #part.plot()
                instrument = part.getInstrument().instrumentName


                #休符と音符
                #for tmptmp in part.flat.notesAndRests:
                #    print(tmptmp.isChord)
                for note in part.flat.notesAndRests:
                    #noteはNoteオブジェクト
                    if note.isChord == True:
                       for chord_note in note.pitches:
                           pitch = chord_note.ps
                           volume = note.volume.realized
                           start = note.offset
                           duration = note.quarterLength
                           strength = note.beatStrength                       
                           if(note.tie != None):
                               if(note.tie.type == "start"):
                                   tmp_xml_list = [start, duration, pitch, strength, volume]
                               elif(note.tie.type == "stop" and pitch == tmp_xml_list[2]):
                                   xml_list.append([tmp_xml_list[0], tmp_xml_list[1] + duration, pitch, tmp_xml_list[3], tmp_xml_list[4], note.measureNumber])
                           else:        
                               if(duration != 0):
                                   xml_list.append([start, duration, pitch, strength, volume, note.measureNumber])#, instrument])

                    elif note.isRest == True:
                       pitch = -1
                       start = note.offset
                       duration = note.quarterLength
                       strength = note.beatStrength
                       
                       if(len(xml_list) > 0):
                           #print(xml_list)
                           if(xml_list[-1][0] != start):
                               xml_list.append([start, duration, pitch, strength, volume, note.measureNumber])


                    else:
                       start = note.offset
                       strength = note.beatStrength
                       duration = note.quarterLength
                       pitch = note.pitch.ps
                       volume = note.volume.realized
                       if(note.tie != None):
                           if(note.tie.type == "start"):
                               tmp_xml_list = [start, duration, pitch, strength, volume]
                           elif(note.tie.type == "stop" and pitch == tmp_xml_list[2]):
                               xml_list.append([tmp_xml_list[0], tmp_xml_list[1] + duration, pitch, tmp_xml_list[3], tmp_xml_list[4], note.measureNumber])
                       else:
                           if(duration != 0):
                               xml_list.append([start, duration, pitch, strength, volume, note.measureNumber])#, instrument])

        xml_list = sorted(xml_list, key=lambda x: (x[0]))
        """
        """
        for i in xml_list:
            print(i)
        """
        return tone_list
        
    def make_data(self, file_name):
        fn = file_name
        original  =  self.getter(fn, 0)        
        start = []
        duration = []
        pitch = []
        beat = []
        
        #元旋律
        for i in original:
            pitch.append(i[0])
            start.append(float(i[1]))
            duration.append(float(i[2]))
            beat.append(i[3])
        
        new_data = []
        new_start = []
        new_pitch = []
        new_duration = []
        new_beat = []
        
        tmp1 = 0
        tmp2 = 0
        key_strength = 0
        
        """
        #連打音を統合
        for i in range(len(pitch)-1):
            if((tmp1 == pitch[i] and tmp2 >= duration[i] and key_strength == 1 and tmp2 + duration[i] == duration[i+1])):
                #print("hello")
                new_duration[-1] += duration[i]
            else:
                new_pitch.append(pitch[i])
                new_duration.append(duration[i])
                new_beat.append(beat[i])
                new_start.append(start[i])
            
            tmp1 = pitch[i]
            tmp2 = duration[i]
            
            if(beat[i] >= 0.25):
                key_strength = 1
            else:
                key_strength = 0
        """
                
        #print(len(new_start))
        #print(len(new_pitch))
        #print(len(new_duration))
        #print(len(new_beat))
        
        return start, pitch, duration, beat