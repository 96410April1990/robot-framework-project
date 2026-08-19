def get_dom_summary(page):

    elements = page.evaluate(
        """
        () => {
            let result=[];

            document.querySelectorAll(
                "button,input,a,select,textarea,[role]"
            )
            .forEach(el=>{

                result.push({

                    tag: el.tagName,
                    text: el.innerText || "",
                    id: el.id || "",
                    class: el.className || "",
                    name: el.getAttribute("name"),
                    placeholder: el.getAttribute("placeholder"),
                    type: el.getAttribute("type"),
                    aria: el.getAttribute("aria-label"),
                    role: el.getAttribute("role")
                
                });
            
            });

            return result;

        }
        """
    )

    return elements