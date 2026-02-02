import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "ArchiPrompt.SearchablePresets",
    async nodeCreated(node) {
        if (node.comfyClass === "JsonPromptNode") {
            node.size[0] = 320;
            setTimeout(() => {
                node.widgets?.forEach(w => {
                    if (w.type === "combo") w.options.searchable = true;
                });
            }, 100);
        }
    }
});
