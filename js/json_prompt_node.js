import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "ArchiPrompt.SearchablePresets",
    
    async nodeCreated(node) {
        if (node.comfyClass !== "JsonPromptNode") {
            return;
        }

        // 适当增加节点宽度，让搜索框和长文件名显示更全
        node.size[0] = 320;

        // 遍历所有 widget，为下拉菜单(combo)开启内置搜索功能
        setTimeout(() => {
            if (node.widgets) {
                node.widgets.forEach(w => {
                    if (w.type === "combo") {
                        // 开启 ComfyUI 内置的搜索支持，不破坏数据传递
                        w.options.searchable = true;
                    }
                });
            }
        }, 100);
    }
});
