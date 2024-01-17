#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import time
import copy
import argparse
import textwrap
import numpy
import dcase_util
dcase_util.utils.setup_logging()

def main(argv):
    # Get logging interface
    log = dcase_util.ui.FancyLogger()

    parser = argparse.ArgumentParser(
        prefix_chars='-+',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            ''' 
            {app_title}
            DCASE DataList
            ---------------------------------------------            
            '''.format(app_title='Audio Stats')
        )
    )

    parser.add_argument("-p", "--path", help="path to dataset folder", required=False)
    args = parser.parse_args()

    log.title('DCASE DataList -- Audio Stats')
    log.line()

    stats = {
        'total_duration': 0,
        'channels': [],
        'formats': [],
        'fs': [],
        'subtype': [],
        'codecs': []
    }
    file_lengths_raw = []

    if args.path:
        audio_files = dcase_util.utils.Path().file_list(path=args.path, extensions=['wav', 'flac'])
        for audio_file in audio_files:
            audio_info = dcase_util.utils.get_audio_info(audio_file)
            print(audio_info)

            if 'channels' in audio_info and audio_info['channels'] not in stats['channels']:
                stats['channels'].append(audio_info['channels'])

            if audio_info['format'] not in stats['formats']:
                stats['formats'].append(audio_info['format'])

            if audio_info['fs'] not in stats['fs']:
                stats['fs'].append(audio_info['fs'])

            stats['total_duration'] += audio_info['duration_sec']

            if audio_info['duration_sec'] not in file_lengths_raw:
                file_lengths_raw.append(audio_info['duration_sec'])

            if 'subtype' in audio_info and audio_info['subtype']['name'] not in stats['subtype']:
                stats['subtype'].append(audio_info['subtype']['name'])
            elif 'codec' in audio_info:
                stats['subtype'].append(audio_info['codec']['name'])

            if 'codec' in audio_info and audio_info['codec']['name'] not in stats['codecs']:
                stats['codecs'].append(audio_info['codec']['name'])

        if file_lengths_raw:
            stats['file_lengths'] = {
                'min': min(file_lengths_raw),
                'max': max(file_lengths_raw),
                'avg': numpy.mean(file_lengths_raw),
                'std': numpy.std(file_lengths_raw)
            }

        log.section_header('Dataset')
        log.data('Path', args.path)
        log.line()
        log.line()

        log.line('data', indent=2)
        log.data('type', 'Audio', indent=4)
        log.line('file_format', indent=4)
        if len(stats['formats']) == 1:
            log.data('type', 'Constant', indent=6)
            log.data('format', stats['formats'][0].lower(), indent=6)
            if stats['formats'][0].lower() == 'wav' or stats['formats'][0].lower() == 'flac':
                log.data('lossy_compression', 'No', indent=6)
            elif stats['codecs']:
                log.data('lossy_compression', 'Yes', indent=6)
            else:
                log.data('lossy_compression', 'Yes', indent=6)

            if stats['subtype'][0] == 'PCM_16':
                log.data('bit_rate', 16, indent=6)
            elif stats['subtype'][0] == 'PCM_24':
                log.data('bit_rate', 24, indent=6)
            elif stats['subtype'][0] == 'PCM_32' or stats['subtype'][0] == 'FLOAT':
                log.data('bit_rate', 32, indent=6)
            elif stats['subtype'][0] == 'DOUBLE':
                log.data('bit_rate', 64, indent=6)
            elif stats['subtype'][0] == 'PCM_S8' or stats['subtype'][0] == 'PCM_U8':
                log.data('bit_rate', 8, indent=6)

        else:
            log.data('type', 'Variable', indent=6)

        if len(stats['fs']) == 1:
            log.data('sampling_rate_khz', stats['fs'][0], indent=6)

        log.line()

        log.line('files', indent=2)
        log.data('total_count', len(audio_files), indent=4)
        log.data('total_duration_minutes', int(stats['total_duration'] / 60.0), indent=4)

        if round(stats['file_lengths']['min'],1) == round(stats['file_lengths']['max'],1):
            log.data('file_length', 'Constant', indent=4)
        elif stats['file_lengths']['min'] / stats['file_lengths']['avg'] > 0.9 and stats['file_lengths']['max'] / stats['file_lengths']['avg'] < 1.1:
            log.data('file_length', 'Quasi-constant', indent=4)
        else:
            log.data('file_length', 'Variable', indent=4)

        log.data('file_length_seconds', '{min}-{max}'.format(min=int(stats['file_lengths']['min']), max=int(stats['file_lengths']['max'])), indent=4)
        log.line()
        log.line()

        print(stats)
        #from IPython import embed
        #embed()

if __name__ == '__main__':
    sys.exit(main(sys.argv))