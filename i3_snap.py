import time
from i3ipc import Connection, Event

# Create the Connection object that can be used to send commands and subscribe
# to events.
i3 = Connection()

# Print the name of the focused window
# focused = i3.get_tree().find_focused()
# print("Focused window %s is on workspace %s" % (focused.name, focused.workspace().name))
#
# # Query the ipc for outputs. The result is a list that represents the parsed
# # reply of a command like `i3-msg -t get_outputs`.
# outputs = i3.get_outputs()
#
# print("Active outputs:")
#
# for output in filter(lambda o: o.active, outputs):
#     print(output.name)
#
# # Send a command to be executed synchronously.
# i3.command("focus left")
#
# # Take all fullscreen windows out of fullscreen
# for container in i3.get_tree().find_fullscreen():
#     container.command("fullscreen")
#
# # Print the names of all the containers in the tree
# root = i3.get_tree()
# print(root.name)
# for con in root:
#     print(con.name)
#
#
# # Define a callback to be called when you switch workspaces.
# def on_workspace_focus(self, e):
#     # The first parameter is the connection to the ipc and the second is an object
#     # with the data of the event sent from i3.
#     if e.current:
#         print("Windows on this workspace:")
#         for w in e.current.leaves():
#             print(w.name)
#
#
# # Dynamically name your workspaces after the current window class
# def on_window_focus(i3, e):
#     focused = i3.get_tree().find_focused()
#     ws_name = "%s:%s" % (focused.workspace().num, focused.window_class)
#     i3.command('rename workspace to "%s"' % ws_name)
#
#
# def on_window_floating(self, e):  # Срабатывает когда окно становится плавающим
#     print(123)
#
#
# def on_window_move(
#     self, e
# ):  # Срабатывает когда окно передвигается НЕ В ПЛАВАЮЩЕМ РЕЖИМЕ
#     print(2281337)


def on_window(self, e):
    window = e.container
    if window.floating == "user_on":
        workspace = i3.get_tree().find_focused().workspace()
        screen_width = workspace.rect.width
        screen_height = workspace.rect.height

        x = window.rect.x
        y = window.rect.y

        workspace_x = workspace.rect.x
        workspace_y = workspace.rect.y
        workspace_width = workspace.rect.width

        print(x, y)

        commands = []

        right_edge = workspace_x + workspace_width
        new_window_x = 0
        if window.rect.x < workspace_x + 60:
            print("Прилипание к левому краю")
            # window.command(f"move position {workspace_x + 5} {y}")
            commands.append(f"move position {workspace_x + 5} {y}")
            new_window_x = workspace_x + 5

        window_right = window.rect.x + window.rect.width

        if window_right > right_edge - 60:
            print(window.rect.x, workspace_width)
            print("Прилипание к правому краю")
            # window.command(f"move position {right_edge - window.rect.width - 5} {y}")
            commands.append(f"move position {right_edge - window.rect.width - 5} {y}")

        if window.rect.y < workspace_y + 60:
            print(window.rect.x, workspace_width)
            print("Прилипание к верхнему краю")
            # window.command(f"move position {x} {workspace_y + 15}")
            if new_window_x:
                commands.append(f"move position {new_window_x} {workspace_y + 15}")
            else:
                commands.append(f"move position {window.rect.x} {workspace_y + 15}")

        for i in commands:
            window.command(i)

        # if window.rect.y < workspace_y + 60:
        #     print("Прилипание к левому краю")
        #     window.command(f"move position {workspace_x} {y}")
        #
        # if window.rect.x < workspace_x + 60:
        #     print("Прилипание к левому краю")
        #     window.command(f"move position {workspace_x} {y}")


# Subscribe to events
# i3.on(Event.WORKSPACE_FOCUS, on_workspace_focus)
# i3.on(Event.WINDOW_FOCUS, on_window_focus)
# i3.on(Event.WINDOW_FLOATING, on_window_floating)
# i3.on(Event.WINDOW_MOVE, on_window_move)
i3.on(Event.WINDOW, on_window)

# Start the main loop and wait for events to come in.
i3.main()
