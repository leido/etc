-----------------------------------------------------------------------------------------------------------------------
--                                                Rules config                                                       --
-----------------------------------------------------------------------------------------------------------------------

-- Grab environment
local awful =require("awful")
local beautiful = require("beautiful")
local redtitle = require("redflat.titlebar")

-- Initialize tables and vars for module
-----------------------------------------------------------------------------------------------------------------------
local rules = {}

rules.base_properties = {
	border_width     = beautiful.border_width,
	border_color     = beautiful.border_normal,
	focus            = awful.client.focus.filter,
	raise            = true,
	size_hints_honor = false,
	screen           = awful.screen.preferred,
}

rules.floating_any = {
	class = { "Nemo", "Gedit" }
}

rules.titlebar_exeptions = {
	class = { "Gnome-terminal" }
}

rules.maximized = {
	class = { "Google-chrome", "Evince"}
}

rules.move_to_edit = {
	class = { "Code" }
}

rules.move_to_full = {
	class = { "Google-chrome"}
}

rules.move_to_main = {
	class = { "Gnome-terminal" }
}

rules.move_to_read = {
	class = { "Evince" }
}

-- applications geometry
------------------------------------------------------------------------------------

local geo = {
	Gedit = { x = 0, y = 10, width = 1000, height = 1000},
	Nemo =  { x = 350, y = 150, width = 1280, height = 720}
}










-- Build rule table
-----------------------------------------------------------------------------------------------------------------------
function rules:init(args)

	local args = args or {}
	self.base_properties.keys = args.hotkeys.keys.client
	self.base_properties.buttons = args.hotkeys.mouse.client


	-- Build rules
	--------------------------------------------------------------------------------
	self.rules = {
		{
			rule       = {},
			properties = args.base_properties or self.base_properties
		},
		{
			rule_any   = args.floating_any or self.floating_any,
			properties = { floating = true },
			callback = function (c)
				c:geometry(geo[c.class])
			end
		},
		{
			rule_any   = self.maximized,
			callback = function(c)
				c.maximized = true
				redtitle.cut_all({ c })
				c.height = c.screen.workarea.height - 2 * c.border_width
			end
		},
		{
			rule_any   = { type = { "normal", "dialog" }},
			except_any = self.titlebar_exeptions,
			properties = { titlebars_enabled = true }
		},
		{
			rule_any   = { type = { "normal" }},
			properties = { placement = awful.placement.no_overlap + awful.placement.no_offscreen }
		},
		{
			rule_any = self.move_to_main,
			properties = { tag = "Main", switchtotag = true }
		},
		{
			rule_any = self.move_to_full,
			properties = { tag = "Full", switchtotag = true }
		},
		{
			rule_any = self.move_to_edit,
			properties = { tag = "Edit", switchtotag = true }
		},
		{
			rule_any = self.move_to_read,
			properties = { tag = "Read", switchtotag = true }
		}

	}


	-- Set rules
	--------------------------------------------------------------------------------
	awful.rules.rules = rules.rules
end

-- End
-----------------------------------------------------------------------------------------------------------------------
return rules
