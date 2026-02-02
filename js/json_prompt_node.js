import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "JsonPromptNode.SearchablePresets",
    
    async nodeCreated(node) {
        if (node.comfyClass !== "JsonPromptNode") {
            return;
        }

        // 更新为中文参数名
        const searchableWidgets = ["透视图", "鸟瞰图", "其他"];
        const nodeWidth = node.size[0] || 300;

        node.widgets.forEach(widget => {
            if (!searchableWidgets.includes(widget.name) || widget.type !== "combo") {
                return;
            }

            const originalValues = [...widget.options.values];
            
            // 标记为可搜索
            widget.options.searchable = true;
            
            // 保持原有搜索增强逻辑...
            if (widget.element) {
                this._enhanceDOMWidget(widget, originalValues, node);
            }
            
            node.size[0] = Math.max(nodeWidth, node.size[0]);
        });
    },

    _enhanceDOMWidget(widget, allValues, node) {
        const element = widget.element;
        if (!element || element.tagName !== "SELECT") return;

        const wrapper = document.createElement("div");
        wrapper.style.cssText = "display:flex;flex-direction:column;width:100%;gap:2px;";

        const searchInput = document.createElement("input");
        searchInput.type = "text";
        searchInput.placeholder = "搜索...";
        searchInput.style.cssText = "padding:4px;border:1px solid #555;border-radius:4px;background:#222;color:#fff;font-size:12px;display:none;";

        const select = element;
        
        const filterOptions = (query) => {
            const filtered = allValues.filter(v => 
                v.toLowerCase().includes(query.toLowerCase())
            );
            
            const currentValue = select.value;
            select.innerHTML = "";
            
            filtered.forEach(val => {
                const option = document.createElement("option");
                option.value = val;
                option.textContent = val;
                select.appendChild(option);
            });
            
            if (filtered.includes(currentValue)) {
                select.value = currentValue;
            }
        };

        searchInput.addEventListener("input", (e) => {
            filterOptions(e.target.value);
        });

        select.addEventListener("mousedown", () => {
            if (searchInput.style.display === "none") {
                searchInput.style.display = "block";
                filterOptions("");
            }
        });

        let blurTimeout;
        searchInput.addEventListener("blur", () => {
            blurTimeout = setTimeout(() => {
                searchInput.style.display = "none";
            }, 200);
        });

        searchInput.addEventListener("focus", () => {
            if (blurTimeout) clearTimeout(blurTimeout);
        });

        if (element.parentNode) {
            element.parentNode.insertBefore(wrapper, element);
            wrapper.appendChild(searchInput);
            wrapper.appendChild(element);
        }
    }
});