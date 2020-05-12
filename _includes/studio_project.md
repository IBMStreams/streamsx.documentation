You\'re ready to start building your application. First, you\'ll create
a Streams project, which is a collection of files in a directory tree in
the Eclipse workspace, and then an application in that project.

The New SPL Application Project wizard takes care of a number of steps
in one pass: it creates a project, a namespace, an SPL source file, and
a main composite.

In Streams, a main composite is an application. Usually, each main
composite lives in its own source file (of the same name), but this is
not required. This section does not explore composite operators or what
distinguishes a main composite from any other composite.

To create a project and a main composite:

1.  Click **File** \> **New** \> **Project**. Alternatively, right-click
    in the Project Explorer and select **New** \> **Project**.
2.  In the New Project dialog, expand **IBM Streams Studio**, and select
    **SPL Application Project**.
3.  Click **Next**.
4.  In the New SPL Application Project wizard, enter the following
    information:
    -   **Project name**: `MyProject`
    -   **Namespace**: `my.name.space`
    -   **Main Composite Name**: `MyMainComposite`
5.  Click **Next**.
6.  On the SPL Project Configuration panel, change the **Toolkit** name
    to `MyToolkit`.
7.  In the **Dependencies** field, clear **Toolkit Locations**.
8.  Click **Finish**.\
    **Project dependencies**: In the **Dependencies** field you can
    signal that an application requires operators or other resources
    from one or more toolkits---a key aspect of the extensibility that
    makes Streams such a flexible and powerful platform. For now, you
    will use only building blocks from the built-in Standard Toolkit.
9.  Check your results.\
    You should see the following items in Streams Studio:
    -   The new project shows in the Project Explorer view on the left.
    -   The code module named MyMainComposite.spl opens in the graphical
        editor with an empty composite named **MyMainComposite** in the
        canvas.
