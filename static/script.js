function calculateFLAMES() {
    let name1 = document.getElementById("name1").value.toLowerCase().replace(/\s+/g, "");
    let name2 = document.getElementById("name2").value.toLowerCase().replace(/\s+/g, "");

    let nameArr1 = name1.split("");
    let nameArr2 = name2.split("");
    
    nameArr1.forEach(letter => {
        let index = nameArr2.indexOf(letter);
        if (index !== -1) {
            nameArr2.splice(index, 1);
            nameArr1.splice(nameArr1.indexOf(letter), 1);
        }
    });
    
    let remainingCount = nameArr1.length + nameArr2.length;
    let flames = ["F", "L", "A", "M", "E", "S"];
    let index = 0;
    
    while (flames.length > 1) {
        index = (index + remainingCount - 1) % flames.length;
        flames.splice(index, 1);
    }
    
    let resultMap = {
        "F": "Friends 🤝👨👩",
        "L": "Lover ❤️💛",
        "A": "Attraction 💖👀",
        "M": "Marriage 👰👨👩",
        "E": "Enemy 💀💥",
        "S": "Sister 👩👩"
    };
    
    document.getElementById("result").innerHTML = `Your Relationship: 
        <span style="background: -webkit-linear-gradient(45deg, #ff6a00, #ee0979);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;">
            ${flames[0]} - ${resultMap[flames[0]].split(" ")[0]}
        </span> 
        ${resultMap[flames[0]].split(" ").slice(1).join(" ")}`;
}

// Theme Toggle
function toggleTheme() {
    document.body.classList.toggle('light-theme');
}
