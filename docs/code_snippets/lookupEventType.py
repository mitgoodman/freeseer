from PyQt4 import QtCore

def lookupEventType(event):
    '''
    @event: QtCore.QEvent
    reverse lookup for events.
    '''
    return {
QtCore.QEvent.AccessibilityDescription: "AccessibilityDescription",
QtCore.QEvent.AccessibilityHelp: "AccessibilityHelp",
QtCore.QEvent.AccessibilityPrepare: "AccessibilityPrepare",
QtCore.QEvent.ActionAdded: "ActionAdded",
QtCore.QEvent.ActionChanged: "ActionChanged",
QtCore.QEvent.ActionRemoved: "ActionRemoved",
QtCore.QEvent.ActivationChange: "ActivationChange",
QtCore.QEvent.ApplicationActivate: "ApplicationActivate",
QtCore.QEvent.ApplicationActivated: "ApplicationActivated",
QtCore.QEvent.ApplicationDeactivate: "ApplicationDeactivate",
QtCore.QEvent.ApplicationFontChange: "ApplicationFontChange",
QtCore.QEvent.ApplicationLayoutDirectionChange: "ApplicationLayoutDirectionChange",
QtCore.QEvent.ApplicationPaletteChange: "ApplicationPaletteChange",
QtCore.QEvent.ApplicationWindowIconChange: "ApplicationWindowIconChange",
QtCore.QEvent.ChildAdded: "ChildAdded",
QtCore.QEvent.ChildPolished: "ChildPolished",
QtCore.QEvent.ChildRemoved: "ChildRemoved",
QtCore.QEvent.Clipboard: "Clipboard",
QtCore.QEvent.Close: "Close",
QtCore.QEvent.CloseSoftwareInputPanel: "CloseSoftwareInputPanel",
QtCore.QEvent.ContextMenu: "ContextMenu",
QtCore.QEvent.CursorChange: "CursorChange",
QtCore.QEvent.DeferredDelete: "DeferredDelete",
QtCore.QEvent.DragEnter: "DragEnter",
QtCore.QEvent.DragLeave: "DragLeave",
QtCore.QEvent.DragMove: "DragMove",
QtCore.QEvent.Drop: "Drop",
QtCore.QEvent.EnabledChange: "EnabledChange",
QtCore.QEvent.Enter: "Enter",
QtCore.QEvent.EnterWhatsThisMode: "EnterWhatsThisMode",
QtCore.QEvent.FileOpen: "FileOpen",
QtCore.QEvent.FocusIn: "FocusIn",
QtCore.QEvent.FocusOut: "FocusOut",
QtCore.QEvent.FontChange: "FontChange",
QtCore.QEvent.GrabKeyboard: "GrabKeyboard",
QtCore.QEvent.GrabMouse: "GrabMouse",
QtCore.QEvent.GraphicsSceneContextMenu: "GraphicsSceneContextMenu",
QtCore.QEvent.GraphicsSceneDragEnter: "GraphicsSceneDragEnter",
QtCore.QEvent.GraphicsSceneDragLeave: "GraphicsSceneDragLeave",
QtCore.QEvent.GraphicsSceneDragMove: "GraphicsSceneDragMove",
QtCore.QEvent.GraphicsSceneDrop: "GraphicsSceneDrop",
QtCore.QEvent.GraphicsSceneHelp: "GraphicsSceneHelp",
QtCore.QEvent.GraphicsSceneHoverEnter: "GraphicsSceneHoverEnter",
QtCore.QEvent.GraphicsSceneHoverLeave: "GraphicsSceneHoverLeave",
QtCore.QEvent.GraphicsSceneHoverMove: "GraphicsSceneHoverMove",
QtCore.QEvent.GraphicsSceneMouseDoubleClick: "GraphicsSceneMouseDoubleClick",
QtCore.QEvent.GraphicsSceneMouseMove: "GraphicsSceneMouseMove",
QtCore.QEvent.GraphicsSceneMousePress: "GraphicsSceneMousePress",
QtCore.QEvent.GraphicsSceneMouseRelease: "GraphicsSceneMouseRelease",
QtCore.QEvent.GraphicsSceneMove: "GraphicsSceneMove",
QtCore.QEvent.GraphicsSceneResize: "GraphicsSceneResize",
QtCore.QEvent.GraphicsSceneWheel: "GraphicsSceneWheel",
QtCore.QEvent.Hide: "Hide",
QtCore.QEvent.HideToParent: "HideToParent",
QtCore.QEvent.HoverEnter: "HoverEnter",
QtCore.QEvent.HoverLeave: "HoverLeave",
QtCore.QEvent.HoverMove: "HoverMove",
QtCore.QEvent.IconDrag: "IconDrag",
QtCore.QEvent.IconTextChange: "IconTextChange",
QtCore.QEvent.InputMethod: "InputMethod",
QtCore.QEvent.KeyPress: "KeyPress",
QtCore.QEvent.KeyRelease: "KeyRelease",
QtCore.QEvent.LanguageChange: "LanguageChange",
QtCore.QEvent.LayoutDirectionChange: "LayoutDirectionChange",
QtCore.QEvent.LayoutRequest: "LayoutRequest",
QtCore.QEvent.Leave: "Leave",
QtCore.QEvent.LeaveWhatsThisMode: "LeaveWhatsThisMode",
QtCore.QEvent.LocaleChange: "LocaleChange",
QtCore.QEvent.MenubarUpdated: "MenubarUpdated",
QtCore.QEvent.MetaCall: "MetaCall",
QtCore.QEvent.ModifiedChange: "ModifiedChange",
QtCore.QEvent.MouseButtonDblClick: "MouseButtonDblClick",
QtCore.QEvent.MouseButtonPress: "MouseButtonPress",
QtCore.QEvent.MouseButtonRelease: "MouseButtonRelease",
QtCore.QEvent.MouseMove: "MouseMove",
QtCore.QEvent.MouseTrackingChange: "MouseTrackingChange",
QtCore.QEvent.Move: "Move",
QtCore.QEvent.Paint: "Paint",
QtCore.QEvent.PaletteChange: "PaletteChange",
QtCore.QEvent.ParentAboutToChange: "ParentAboutToChange",
QtCore.QEvent.ParentChange: "ParentChange",
QtCore.QEvent.Polish: "Polish",
QtCore.QEvent.PolishRequest: "PolishRequest",
QtCore.QEvent.QueryWhatsThis: "QueryWhatsThis",
QtCore.QEvent.RequestSoftwareInputPanel: "RequestSoftwareInputPanel",
QtCore.QEvent.Resize: "Resize",
QtCore.QEvent.Shortcut: "Shortcut",
QtCore.QEvent.ShortcutOverride: "ShortcutOverride",
QtCore.QEvent.Show: "Show",
QtCore.QEvent.ShowToParent: "ShowToParent",
QtCore.QEvent.SockAct: "SockAct",
QtCore.QEvent.StateMachineSignal: "StateMachineSignal",
QtCore.QEvent.StateMachineWrapped: "StateMachineWrapped",
QtCore.QEvent.StatusTip: "StatusTip",
QtCore.QEvent.StyleChange: "StyleChange",
QtCore.QEvent.TabletMove: "TabletMove",
QtCore.QEvent.TabletPress: "TabletPress",
QtCore.QEvent.TabletRelease: "TabletRelease",
QtCore.QEvent.OkRequest: "OkRequest",
QtCore.QEvent.TabletEnterProximity: "TabletEnterProximity",
QtCore.QEvent.TabletLeaveProximity: "TabletLeaveProximity",
QtCore.QEvent.Timer: "Timer",
QtCore.QEvent.ToolBarChange: "ToolBarChange",
QtCore.QEvent.ToolTip: "ToolTip",
QtCore.QEvent.ToolTipChange: "ToolTipChange",
QtCore.QEvent.UngrabKeyboard: "UngrabKeyboard",
QtCore.QEvent.UngrabMouse: "UngrabMouse",
QtCore.QEvent.UpdateLater: "UpdateLater",
QtCore.QEvent.UpdateRequest: "UpdateRequest",
QtCore.QEvent.WhatsThis: "WhatsThis",
QtCore.QEvent.WhatsThisClicked: "WhatsThisClicked",
QtCore.QEvent.Wheel: "Wheel",
QtCore.QEvent.WinEventAct: "WinEventAct",
QtCore.QEvent.WindowActivate: "WindowActivate",
QtCore.QEvent.WindowBlocked: "WindowBlocked",
QtCore.QEvent.WindowDeactivate: "WindowDeactivate",
QtCore.QEvent.WindowIconChange: "WindowIconChange",
QtCore.QEvent.WindowStateChange: "WindowStateChange",
QtCore.QEvent.WindowTitleChange: "WindowTitleChange",
QtCore.QEvent.WindowUnblocked: "WindowUnblocked",
QtCore.QEvent.ZOrderChange: "ZOrderChange",
QtCore.QEvent.KeyboardLayoutChange: "KeyboardLayoutChange",
QtCore.QEvent.DynamicPropertyChange: "DynamicPropertyChange",
QtCore.QEvent.TouchBegin: "TouchBegin",
QtCore.QEvent.TouchUpdate: "TouchUpdate",
QtCore.QEvent.TouchEnd: "TouchEnd",
QtCore.QEvent.WinIdChange: "WinIdChange",
QtCore.QEvent.Gesture: "Gesture",
QtCore.QEvent.GestureOverride: "GestureOverride"}[event.type()]
