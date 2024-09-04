function copy_subtitle()
    local subtitle = mp.get_property("sub-text")
    if subtitle and subtitle ~= "" then
        local platform = detect_platform()
        if platform == "windows" then
            os.execute(string.format('powershell -command "Set-Clipboard -Value \'%s\'"', subtitle:gsub("'", "''")))
        elseif platform == "macos" then
            os.execute(string.format("echo '%s' | pbcopy", subtitle:gsub("'", "'\\''")))
        elseif platform == "linux" then
            os.execute(string.format("echo '%s' | xclip -selection clipboard", subtitle:gsub("'", "'\\''")))
        end
        mp.osd_message("Subtitle copied to clipboard")
    end
end

function detect_platform()
    local o = {}
    if mp.get_property_native('options/vo-mmcss-profile', o) ~= o then
        return 'windows'
    elseif mp.get_property_native('options/cocoa-force-dedicated-gpu', o) ~= o then
        return 'macos'
    end
    return 'linux'
end

mp.add_key_binding("c", "copy-subtitle", copy_subtitle)
