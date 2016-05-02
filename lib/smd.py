# smd.py, smd/lib/
# smd: sceext's markdown style

from . import log

from . import smd_config


# entry function
def smd_compile(raw):
    '''
    
    -> str
    '''
    
    raw = _c_remove_xml_comment(raw)
    raw = _c_normal_line_ending(raw)
    
    # do split lines
    lines = raw.split('\n')
    # check first line
    _check_first_line(lines)
    
    # first process lines
    lines = _c_process_line(lines)
    lines = _c_check_concat_line(lines)
    lines = _c_second_process(lines)
    
    # process done
    out = _c_concat_line(lines)
    return out

# check functions

def _check_first_line(lines):
    first = ''
    if len(lines) > 0:
        first = lines[0]
    OK_F = smd_config.SMD_FIRST_LINE_START
    if not first.startswith(OK_F):
        # log WARNING here
        log.w('this document is not in smd format, the first line \"' + first + '\" not startswith \"' + OK_F + '\" ')
        
        return False	# check not pass
    return True	# check pass

def check_file_name(name):
    OK_EXT = smd_config.SMD_FILE_EXT
    if not name.endswith(OK_EXT):
        # log WARNING here
        log.w('ext of this file \"' + name + '\" is not \"' + OK_EXT + '\" ')
        
        return False	# check not pass
    return True	# check pass

# base compile functions

def _c_concat_line(lines):
    out = ''
    for l in lines:
        out += l['text']
    return out

def _c_remove_xml_comment(raw):
    '''
    remove xml comment format
    <!-- -->
    
    -> str
    '''
    CS = smd_config.SMD_COMMENT_START
    CE = smd_config.SMD_COMMENT_END
    
    rest = raw
    flag_comment = False
    
    out = ''
    while len(rest) > 0:
        if flag_comment:
            # NO -->
            if not CE in rest:
                rest = ''
                continue
            # split by -->
            one, rest = rest.split(CE, 1)
            out += one
            flag_comment = False	# reset flag
            continue
        # check no <!--
        if not CS in rest:
            out += rest
            rest = ''
            continue
        # split by <!--
        one, rest = rest.split(CS, 1)
        out += one
        flag_comment = True
    return out

def _c_normal_line_ending(raw):
    '''
    replace abnormal line-ending chars
    \r\n -> \n
    \r -> \n
    
    -> str
    '''
    out = raw.replace('\r\n', '\n').replace('\r', '\n')
    return out

# first process smd lines
def _c_process_line(raw):
    FC = smd_config.SMD_LINE_FRIST_CHAR
    
    out = []
    # check each line
    for i in range(len(raw)):
        line = raw[i]
        # check line is null
        if len(line) < 1:
            one = {
                'type' : '', 
                'text' : '', 
                'index' : i, 	# line number of src file FIXME BUG here
            }
            out.append(one)
            continue
        # check first char
        first, rest = line[0], line[1:]
        if first == FC['comment']:
            # ignore comment line
            continue
        elif first == FC['title']:
            # add \n before and after title line
            one = {
                'type' : 'skip', 
                'text' : '\n', 
                'index' : i, 
            }
            out.append(one)
            one = {
                'type' : '', 
                'text' : line, 
                'index' : i, 
            }
            out.append(one)
            one = {
            	'type' : 'skip', 
            	'text' : '\n', 
            	'index' : i, 
            }
            out.append(one)
        elif first == FC['p']:
            # add \n before this line
            one = {
                'type' : 'skip', 
                'text' : '\n', 
                'index' : i, 
            }
            out.append(one)
            one = {
                'type' : 'skip', 
                'text' : rest, 
                'index' : i, 
            }
            out.append(one)
        else:	# add normal line
            one = {
                'type' : '', 
                'text' : line, 
                'index' : i, 
            }
            out.append(one)
    return out

# check and concat same type lines
def _c_check_concat_line(raw):
    out = []
    # put first line
    one = {
        'type' : '', 
        'text' : '', 
        'index' : -1, 
    }
    out.append(one)
    
    rest = raw
    while len(rest) > 0:
        one, rest = rest[0], rest[1:]
        if (one['type'] == '') and (out[-1]['type'] == ''):
            # concat normal line, add space char
            out[-1]['text'] += ' ' + one['text']
        else:	# not concat
            out.append(one)
    return out

# process after first line process
def _c_second_process(raw):
    # process each line
    for i in raw:
        if i['type'] != 'skip':
            i['text'] = _c_scan_clip(i['text'], i['index'])
    return raw

# scan a small pice of text, and return result
def _c_scan_clip(raw, line_n):
    SC = smd_config.SMD_SLASH_CHAR
    BC = smd_config.SMD_BEFORE_CHAR
    AC = smd_config.SMD_AFTER_CHAR
    
    rest = raw
    flag_s = False	# for \ char
    flag_u = False	# for _ char
    
    out = ''
    # scan each char
    while len(rest) > 0:
        one, rest = rest[0], rest[1:]
        # check \ mode
        if flag_s:
            if not one in SC:
                log.w('unknow slash char [\\' + one + '] at line ' + str(line_n) + ': ' + raw + '')
                # NOTE just ignore bad char
            else:	# do replace
                out += SC[one]
            flag_s = False	# reset flag
            continue
        elif flag_u:	# _ mode
            if not one in BC:
                # add as normal char
                out += '_' + one
            else:
                out += BC[one]
            flag_u = False	# reset flag
            continue
        # check \ char
        if one == '\\':
            flag_s = True	# set flag
            continue
        # check _ char
        if one == '_':
            flag_u = True	# set flag
            continue
        # check chars before _ char
        if one in AC:
            # check next is _ char
            if rest.startswith('_'):
                out += AC[one]
                rest = rest[1:]	# reset rest
            else:
                # add as normal char
                out += one
            continue
        # check multi-space chars
        if one == ' ':
            if not out.endswith(' '):
                out += ' '
            continue
        # normal char
        out += one
    return out	# done

# end smd.py


