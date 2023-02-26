// Lets Start JS

function ChangeMatchColour(result, match_id)
{
    let match = 'match-'.concat(match_id);
    let stats_button = 'stats-button-'.concat(match_id);

    if (result == 'win'){
        document.getElementById(match).classList.add('match-win');
        document.getElementById(stats_button).classList.add('stats-button-win');
    }
    else if (result == 'lose'){
        document.getElementById(match).classList.add('match-lose');
        document.getElementById(stats_button).classList.add('stats-button-lose');
    }
    else{
        document.getElementById(match).classList.add('match-remake');
        document.getElementById(stats_button).classList.add('stats-button-remake');
    }
}

function ChangeDisplay(match_id)
{
    let match = 'all-stats-'.concat(match_id);
    let stats = 'stats-button-'.concat(match_id);
    let match_display = document.getElementById(match);
    let stats_Button = document.getElementById(stats);

    if (match_display.style.display === 'none') {
        match_display.style.display = 'grid';
        stats_Button.innerHTML = "<p>&#9651;</p>";
    } else {
        match_display.style.display = 'none';
        stats_Button.innerHTML = "<p>&#9661;</p>";
    }
}
