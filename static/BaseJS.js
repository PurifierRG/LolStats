// Lets Start JS

function ChangeMatchColour(result, match_id)
{
    let match = 'match-'.concat(match_id);

    if (result == 'win')
        document.getElementById(match).classList.add('match-win')
    else
        document.getElementById(match).classList.add('match-lose')
}
