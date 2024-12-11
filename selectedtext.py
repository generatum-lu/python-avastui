# https://stackoverflow.com/questions/1007185/how-to-retrieve-the-selected-text-from-the-active-window
import array
import ctypes as ct
from ctypes import wintypes as wt
from time import sleep

#import win32gui
# import pywin32
# import win32api
#import win32con

import win32gui as wgui
import win32process as wproc
import win32con as wcon

import sys

from win32api import HIWORD, LOWORD


class GUITHREADINFO(ct.Structure):
    _fields_ = [
        ("cbSize", wt.DWORD),
        ("flags", wt.DWORD),
        ("hwndActive", wt.HWND),
        ("hwndFocus", wt.HWND),
        ("hwndCapture", wt.HWND),
        ("hwndMenuOwner", wt.HWND),
        ("hwndMoveSize", wt.HWND),
        ("hwndCaret", wt.HWND),
        ("rcCaret", wt.RECT),

    ]

    def __str__(self):
        ret = "\n" + self.__repr__()
        start_format = "\n  {0:s}: "
        for field_name, _ in self. _fields_[:-1]:
            field_value = getattr(self, field_name)
            field_format = start_format + ("0x{1:016X}" if field_value else "{1:}")
            ret += field_format.format(field_name, field_value)
        rc_caret = getattr(self, self. _fields_[-1][0])
        ret += (start_format + "({1:d}, {2:d}, {3:d}, {4:d})").format(self. _fields_[-1][0], rc_caret.top, rc_caret.left, rc_caret.right, rc_caret.bottom)
        return ret

#def get_selected_text_from_front_window(*argv): # As String
def get_selected_text_from_front_window(): # As String

    #print('get_selected_text_from_front_window')
    # GUITHREADINFO
    # Enthält Informationen zu einem GUI-Thread.
    #gui = GUITHREADINFO(cbSize=sizeof(GUITHREADINFO))

    # https://stackoverflow.com/questions/59884688/getguithreadinfo-with-pywin32
    #window_name = "Untitled - Notepad"
    #hwnd = wgui.FindWindowEx(wcon.NULL, 0, wcon.NULL, window_name)
    #print("'{0:s}' window handle: 0x{1:016X}".format(window_name, hwnd))
    #tid, pid = wproc.GetWindowThreadProcessId(hwnd)
    #print("PId: {0:d}, TId: {1:d}".format(pid, tid))

    user32_dll = ct.WinDLL("user32.dll")
    GetGUIThreadInfo = getattr(user32_dll, "GetGUIThreadInfo")
    GetGUIThreadInfo.argtypes = [wt.DWORD, ct.POINTER(GUITHREADINFO)]
    GetGUIThreadInfo.restype = wt.BOOL

    gti = GUITHREADINFO()
    gti.cbSize = ct.sizeof(GUITHREADINFO)
    # res = GetGUIThreadInfo(tid, ct.byref(gti))
    res = GetGUIThreadInfo(0, ct.byref(gti))
    #print("{0:s} returned: {1:d}".format(GetGUIThreadInfo.__name__, res))
    #if res:
    #    print(gti)

    #print('gui.cbSize: ' + str(gti.cbSize))
    #print('res: ' + str(res))
    #print('gui: ' + str(gti))
    txt=''
    ast_Clipboard_Obj=None
    Last_Clipboard_Temp = -1

    # GetGUIThreadInfo
    # Ruft Informationen zum aktiven Fenster oder einem angegebenen GUI-Thread ab.
    # [in] idThread: Wenn dieser Parameter NULL ist, gibt die Funktion Informationen für den Vordergrundthread zurück.
    # [in, out] pgui: Ein Zeiger auf eine GUITHREADINFO-Struktur , die Informationen empfängt, die den Thread beschreiben. Beachten Sie, dass Sie das cbSize-Element auf festlegen müssen, sizeof(GUITHREADINFO) bevor Sie diese Funktion aufrufen.
    # byref: Damit wird nicht eine Kopie der Originalvariable übergeben, sondern auf die Originalvariable gezeigt.
    # user32.GetGUIThreadInfo(0, byref(gui))
    #print('user32.GetForegroundWindow(): ' + str(user32.GetForegroundWindow()))
    #print('user32.GetWindowThreadProcessId(user32.GetForegroundWindow(),0): ' + str(user32.GetWindowThreadProcessId(user32.GetForegroundWindow(),0)))
    #print('user32.GetGUIThreadInfo(user32.GetWindowThreadProcessId(user32.GetForegroundWindow(),0), byref(gui)): ' + str(user32.GetGUIThreadInfo(user32.GetWindowThreadProcessId(user32.GetForegroundWindow(),0), byref(gui))))
    # Wenn die Funktion erfolgreich ist, ist der Rückgabewert ungleich Null.
    # Wenn die Funktion fehlerhaft ist, ist der Rückgabewert null. Um erweiterte Fehlerinformationen zu erhalten, rufen Sie GetLastError auf.
    #user32.GetGUIThreadInfo(user32.GetWindowThreadProcessId(user32.GetForegroundWindow(),0), byref(gui))
    # print('GetLastError(): ' + str(GetLastError()))
    # Systemfehlercodes
    # https://learn.microsoft.com/de-de/windows/win32/debug/system-error-codes
    # https://learn.microsoft.com/de-de/windows/win32/debug/system-error-codes--0-499-
    # ERROR_INVALID_PARAMETER
    # 87 (0x57)
    # „Der Parameter ist falsch.“

    # hwndCaret
    # Typ: HWND
    # Ein Handle für das Fenster, das das Caret anzeigt.

    # txt = "Mein Test Text"
    txt = GetCaretWindowText(gti.hwndCaret, True)
    # print('hier')
    # txt = GetCaretWindowText(gti.hwndFocus, True)
    #print('txt: ' + str(txt))

    #del gti

    '''
    if Txt = "" Then
        LastClipboardClip = ""
        Last_Clipboard_Obj = GetClipboard
        Last_Clipboard_Temp = LastClipboardFormat
        SendKeys "^(c)"
        GetClipboard
        Txt = LastClipboardClip
        if LastClipboardClip <> "" Then Txt = LastClipboardClip
        RestoreClipboard Last_Clipboard_Obj, Last_Clipboard_Temp
        print "clbrd: " + Txt
    End If
    '''

    #print('returning text.........')
    return txt



def GetCaretWindowText(hWndCaret, Selected = False): # As String
    #print('GetCaretWindowText')
    #print('hWndCaret: ' + str(hWndCaret))
    #print('Selected: ' + str(Selected))

    buf_size = 0
    text = ""
    #startpos =0
    #endpos =0

    # https://www.programcreek.com/python/example/115374/win32con.WM_GETTEXT
    # buffer_len = SendMessage(hwnd, WM_GETTEXTLENGTH, 0, 0) + 1
    # buffer = array.array('b', b'\x00\x00' * buffer_len)
    # text_len = SendMessage(hwnd, WM_GETTEXT, buffer_len, buffer)
    # text = PyGetString(buffer.buffer_info()[0], buffer_len - 1)
    # return text

    if hWndCaret:
        #print('hWndCaret')
        buf_size = wgui.SendMessage(hWndCaret, wcon.WM_GETTEXTLENGTH, 0, 0) + 1
        #buf_size = wgui.SendMessage(hWndCaret, wcon.WM_GETTEXTLENGTH, 0, 0) + 2
        #buf_size = wgui.SendMessage(hWndCaret, wcon.WM_GETTEXTLENGTH, 0, 0) * 2 + 2
        #print('buf_size: ' + str(buf_size))
        if buf_size:
            #print('buf_size...')
            # https://stackoverflow.com/questions/53182704/python-memorybuffer-pywin32
            #try:
                # print('wgui.PyMakeBuffer(buf_size)...')
                # buffer = wgui.PyMakeBuffer(buf_size)      # hier ist der Fehler: (0xC0000005) ein Programm versucht, auf einen Speicherbereich zuzugreifen, der nicht für es reserviert ist
            #print("array.array('b', b'\x00\x00' * buf_size)")
            buffer = array.array('b', b'\x00\x00' * buf_size)
                #except ValueError:
                #    print('error: wgui.PyMakeBuffer(buf_size)')
                #    return
            #print('buffer: ' + str(buffer))
            text_len = wgui.SendMessage(hWndCaret, wcon.WM_GETTEXT, buf_size, buffer)
            #text = buffer[:buf_size]
            #print('text: ' + str(text))
            #try:
            #    address, length = wgui.PyGetBufferAddressAndLen(buffer)
            #except ValueError:
            #    print('error: wgui.PyGetBufferAddressAndLen(buffer)')
            #    return
            #text = wgui.PyGetString(address, length)
            #text = wgui.PyGetString(buffer.buffer_info()[0], buf_size - 1)
            text = wgui.PyGetString(buffer.buffer_info()[0], text_len)
            #split_text = text.split("\r\n")
            #print('split_text: ' + str(split_text))
            #clean_text = "".join(split_text)
            #print('clean_text: ' + clean_text)
            #print('###########################################################')
            #buffer.release()
            #del buffer
            #address.release()
            #del address
            #length.release()
            #del length
            #print('returning text...')   # dann folgt: 0xC0000374 Code 0xC0000374 is STATUS_HEAP_CORRUPTION (A heap has been corrupted.)
                                         # The "heap" is just where most programs keep all of their data. A "heap corruption" means that some memory in the heap doesn't make any sense. This is almost certainly an indication of a bug in the program's code,
            # return text


        if Selected and buf_size:
            #print('selected and buf_size')
            #print('startpos: ' + str(startpos))
            #print('endpos: ' + str(endpos))
            selinfo  = wgui.SendMessage(hWndCaret, wcon.EM_GETSEL, 0, 0)
            #print('selinfo: ' + str(selinfo))
            #endpos   = win32api.HIWORD(selinfo)
            #endpos   = pywin32.HIWORD(selinfo)
            endpos   = HIWORD(selinfo)
            #startpos = win32api.LOWORD(selinfo)
            #startpos = pywin32.LOWORD(selinfo)
            startpos = LOWORD(selinfo)
            #print('startpos: ' + str(startpos))
            #print('endpos: ' + str(endpos))
            rn1 = text[0:endpos].count("\r\n")
            rn2 = text[startpos:endpos].count("\r\n")
            #print('rn1: ' + str(rn1))
            #print('rn2: ' + str(rn2))
            # print('text[startpos:endpos]:' + (text[startpos+rn:endpos+rn]))
            if rn1 == rn2:
                text = text[startpos:endpos+rn2]
            elif rn1 != rn2:
                text = text[startpos+rn1:endpos+rn1+rn2]
            return text

    #print('returning text......')
    return text

#if __name__ == '__main__':
#    while True:
#        #print('text: ' + get_selected_text_from_front_window())
#        # print('get_selected_text_from_front_window():')
#        myText = get_selected_text_from_front_window()
#        print('myText:' + myText)
#        sleep(5)

if __name__ == "__main__":
    while True:
        #print("Python {0:s} {1:d}bit on {2:s}".format(" ".join(item.strip() for item in sys.version.split("\n")), 64 if sys.maxsize > 0x100000000 else 32, sys.platform))
        #print('Beginn')
        #get_selected_text_from_front_window(*sys.argv[1:])
        mySelectedText = get_selected_text_from_front_window()
        print('mySelectedText: ' + mySelectedText)
        sleep(1)
        #print('Ende')


    #//Get the text from the active window into the stringbuilder
    #SendMessage(focused, WM_GETTEXT, builder.Capacity, builder);
    #Console.WriteLine("Text in active window was " + builder);
    #builder.Append(" Extra text");
    #//Change the text in the active window
    #SendMessage(focused, WM_SETTEXT, 0, builder);
    #Console.ReadKey();