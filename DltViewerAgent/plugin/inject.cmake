# Injected into the upstream dlt-viewer project via CMAKE_PROJECT_dlt-viewer_INCLUDE so the
# plugin builds alongside the bundled plugins without modifying upstream sources.
# Deferred to the end of the top-level directory so the qdlt target and add_plugin() exist.
set(DLT_AGENT_PLUGIN_DIR "${CMAKE_CURRENT_LIST_DIR}")

function(dlt_agent_add_plugin)
    add_library(aiagentplugin MODULE
        "${DLT_AGENT_PLUGIN_DIR}/aiagentplugin.cpp"
        "${DLT_AGENT_PLUGIN_DIR}/agentbridge.cpp"
        "${DLT_AGENT_PLUGIN_DIR}/agentpanel.cpp")
    set_target_properties(aiagentplugin PROPERTIES AUTOMOC ON)
    target_link_libraries(aiagentplugin qdlt
        ${QT_PREFIX}::Widgets
        ${QT_PREFIX}::Network
        ${QT_PREFIX}::Concurrent)
    add_plugin(aiagentplugin)
endfunction()

cmake_language(DEFER CALL dlt_agent_add_plugin)
