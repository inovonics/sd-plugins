sd-plugins
==========

Plugins that we've written or borrowed for the Server Density monitoring agent.

Installation
------------

1.  Checkout repo to `/var/lib/sd-agent`.

2.  Set the permissions on the checked out folder:

        chown -R sd-agent:sd-agent /var/lib/sd-agent
        chmod -R 0775 /var/lib/sd-agent

3.  Concatenate `plugins.cfg` from the repository to `plugins.cfg` in the agent configuration directory.  Don't forget
    update the `plugins.cfg` file afterwards to enable the desired plugins.

4.  Update the agent configuration to point to the plugins directory:

        plugin_directory: /var/lib/sd-agent/plugins

5.  Restart the agent.
