import { app } from "../../scripts/app.js";

// 用于确保前端与后端参数名严格对应
const SEARCHABLE_WIDGETS = ["透视图", "鸟瞰图", "其他"];

app.registerExtension({
    name: "ArchiPrompt.SearchablePresets",
    
    async nodeCreated(node) {
        if (node.comfyClass !== "JsonPromptNode") {
            return;
        }

        // 稍微加宽节点，防止搜索框太挤
        node.size[0] = 350;

        node.widgets.forEach(widget => {
            // 匹配下拉菜单且在搜索名单内
            if (SEARCHABLE_WIDGETS.includes(widget.name) && widget.type === "combo") {
                
                // 启用内置的可搜索属性（部分 ComfyUI 版本原生支持）
                widget.options.searchable = true;

                // 如果你想保留自定义搜索框，仅在必要时添加
                // 这里的逻辑已简化，避免破坏原始 widget 的数据连通性
                const originalCallback = widget.callback;
                widget.callback = function() {
                    if (originalCallback) return originalCallback.apply(this, arguments);
                };
            }
        });
    }
});
