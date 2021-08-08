const cards = 11
var original = document.getElementById("template");
var clone = original.cloneNode(true);
clone.removeAttribute("id");

original.setAttribute("id","card0")

// Random integers, min included, max excluded
function getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min) ) + min;
}

let targets;

let not_found = true;

let temp;

while (not_found) {
    targets = [4*getRndInteger(3,8)+1]
    not_found = false;
    for (let i = 1; i < cards; i++) {
        targets.push(4*getRndInteger(7,40)+1);
    }
    targets.sort((a, b) => a - b);
    for (let i = 0; i < targets.length - 1; i++) {
        if (targets[i] == targets[i+1]) {
            not_found = true
        }
    }
}

targets[2] += 2

temp = targets[3]
targets[3] = targets[4]
targets[4] = temp
targets[5] -= 1
targets[cards-2] = 4*getRndInteger(130,230)+1

for (let i = 1; i < cards; i++){
  let clone = original.cloneNode(true);
  clone.removeAttribute("id");
  clone.setAttribute("id","card"+i);
  
  document.getElementById("card-contents").appendChild(clone);
}

for (let i = 0; i < cards; i++){
  let card = document.getElementById(`card${i}`);
  let html = card.innerHTML;
  html = html.replace("Target: ", `Target: ${targets[i]}`);
  html = html.replace(`id="target0"`,`id="target${i}"`);
  html = html.replace(`id="ox0"`,`id="ox${i}"`);
  html = html.replace(`id="hyd1-0"`,`id="hyd1-${i}"`);
  html = html.replace(`id="hyd2-0"`,`id="hyd2-${i}"`);
  html = html.replace(`id="message0"`,`id="message${i}"`);
  html = html.replace(`id="imp0"`,`id="imp${i}"`);
  html = html.replace(`id="check0"`,`id="check${i}"`);
  card.innerHTML = html;
}

for (let i = 0; i < targets.length; i++) {
  var check = document.getElementById('check'+i); // is a node
  check.param = i;
  check.addEventListener("click", myScript);
}

function myScript(evt) {
  var i = evt.currentTarget.param;
  let ox = document.getElementById('ox'+i)
  let hyd1 = document.getElementById('hyd1-'+i)
  let hyd2 = document.getElementById('hyd2-'+i)
  let message = document.getElementById('message'+i)
  if ((ox.value.length == 0) || (hyd1.value.length == 0) || (hyd2.value.length == 0)) {
    message.innerHTML = "Fill in the three values!"
  } else if (ox.value != 5) {
    message.innerHTML = "The oxygen value is not right."
  }
  else if (hyd1.value != hyd2.value) {
    message.innerHTML = "The hydrogen values must be equal!"
  } else if (hyd1.value % 2 != 0) {
    message.innerHTML = "The hydrogen values must be even!"
  } else if (hyd1.value < 1) {
    message.innerHTML = "The hydrogen values must be positive!"
  }else if (Number(ox.value) + 2*Number(hyd1.value) != targets[i]) {
      message.innerHTML = `Not quite.  Your total: ${Number(ox.value) + 2*Number(hyd1.value)}<br><i class="far fa-sad-cry fa-3x cyan-text pr-3"></i>`
  } else if (Number(ox.value) + 2*Number(hyd1.value) == targets[i]) {
    message.innerHTML = `Great work!  Your total: ${Number(ox.value) + 2*Number(hyd1.value)}<br><i class="far fa-laugh-beam fa-3x text-success pr-3"></i>`
  }
}

for (let i = 0; i < targets.length; i++) {
  var check = document.getElementById('imp'+i); // is a node
  check.param = i;
  check.addEventListener("click", myImpScript);
}

function myImpScript(evt) {
  let i = evt.currentTarget.param;
  let message = document.getElementById('message'+i)
  if ((targets[i]%4 == 1)&&(targets[i]>8)) {
      message.innerHTML = ("There is a solution... can you find it?")
  } else {
      message.innerHTML = `Nice job!  This one was impossible; it had no solution!`
  }
}

{
  let i = targets.length-1;
  let custom_target = document.getElementById(`target${i}`);
  let html;
  html = `Choose your own!<br><form class="pure-form" onsubmit="return false">
  <input type="number" id="custom" class="pure-input-rounded" placeholder="" style="text-align: left;"/>
  </form>`;
  custom_target.innerHTML = html;
  custom_target.addEventListener('keyup',newTarget)

  function newTarget(evt){
    let t = document.getElementById('custom').value;
    targets[targets.length-1] = parseInt(t,10);
  }
}

// var temp = $('.card')[3]

// var temp2 = $("#card3 .hyd")