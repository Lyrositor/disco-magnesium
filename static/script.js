class Skill {
    constructor(label, category) {
        this.label = label
        this.category = category
    }
}

const SKILLS = {
    'logic': new Skill('Logic', 'intellect'),
    'encyclopedia': new Skill('Encyclopedia', 'intellect'),
    'rhetoric': new Skill('Rhetoric', 'intellect'),
    'drama': new Skill('Drama', 'intellect'),
    'conceptualization': new Skill('Conceptualization', 'intellect'),
    'visualcalculus': new Skill('Visual Calculus', 'intellect'),

    'volition': new Skill('Volition', 'psyche'),
    'inlandempire': new Skill('Inland Empire', 'psyche'),
    'empathy': new Skill('Empathy', 'psyche'),
    'authority': new Skill('Authority', 'psyche'),
    'espritdecorps': new Skill('Esprit de Corps', 'psyche'),
    'suggestion': new Skill('Suggestion', 'psyche'),

    'endurance': new Skill('Endurance', 'physique'),
    'painthreshold': new Skill('Pain Threshold', 'physique'),
    'physicalinstrument': new Skill('Physical Instrument', 'physique'),
    'electrochemistry': new Skill('Electrochemistry', 'physique'),
    'shivers': new Skill('Shivers', 'physique'),
    'halflight': new Skill('Half Light', 'physique'),

    'handeyecoordination': new Skill('Hand/Eye Coordination', 'motorics'),
    'perception': new Skill('Perception', 'motorics'),
    'reactionspeed': new Skill('Reaction Speed', 'motorics'),
    'savoirfaire': new Skill('Savoir Faire', 'motorics'),
    'interfacing': new Skill('Interfacing', 'motorics'),
    'composure': new Skill('Composure', 'motorics'),
}

const STATE_SIMPLE_ATTRIBUTES = [
    'show_all',
    'show_conditions',
    'money',
    'day',
    'time',
    'damage_health',
    'damage_morale',
    'is_kim_here',
    'is_cuno_in_party',
    'is_raining',
    'is_snowing',
    'is_hardcore',
    'has_beaten_hardcore'
]

function init() {
    window.conversations = []
    window.items = []
    window.variables = {}
    window.state = null
    window.currentAuthor = null
    window.currentColor = null

    $.getJSON('api/init').done(function (result) {
        window.conversations = result.conversations
        window.items = result.items
        window.variables = result.variables
        window.state = result.state
        setupRoot()
        setupVariableInputs()
        applyState()
        setupActions()
        route()
    });

    $(window).on('hashchange', route);
}

function route() {
    const pathElements = window.location.hash.trim().split('/')
    if (pathElements.length < 2 || pathElements[1] === '') {
        showRoot()
    } else if (pathElements.length >= 3 && pathElements.length <= 4) {
        const conversationId = parseInt(pathElements[1])
        const nodeId = parseInt(pathElements[2])
        const roll = pathElements.length === 4 ? pathElements[3] : null
        advanceConversation(conversationId, nodeId, roll)
    } else {
        console.error('Invalid route, returning to root')
        showRoot()
    }
}

function setupActions() {
    $('#save').click(function () {
        localStorage.setItem('state', JSON.stringify(window.state))
    })
    $('#load').click(function () {
        const savedState = localStorage.getItem('state')
        if (savedState != null) {
            window.state = JSON.parse(savedState)
            window.currentAuthor = null
            window.currentColor = null
            applyState()
            clearConversation()
            route()
        }
    })
    $('#state-toggle').click(function () {
        $('#state-overlay').toggle()
        this.text = this.text === 'edit' ? 'close' : 'edit'
    })
    $('#actions').show()
}

function setupRoot() {
    const lists = {
        'exchange': $('#list-exchanges'),
        'thought': $('#list-thoughts'),
        'orb': $('#list-orbs'),
        'bark': $('#list-barks')
    }

    // Hack: force display of conditions when rendering the root
    const original_show_conditions = window.state.show_conditions
    window.state.show_conditions = true
    for (const conversation of window.conversations.sort((a, b) => a.title.localeCompare(b.title))) {
        if (lists.hasOwnProperty(conversation.type)) {
            const option = buildOption(
                conversation.id, conversation.start_node_id, conversation.title, 'regular', conversation.condition
            )
            if (conversation.skill != null && conversation.difficulty_descriptor != null && conversation.difficulty != null) {
                const skill = SKILLS[conversation.skill]
                let label = `${skill.label} - ${conversation.difficulty_descriptor} ${conversation.difficulty}`
                if (conversation.difficulty === 0) {
                    label = `${skill.label}`
                }
                option.find(">:first-child").prepend(
                    $(`<span class="option-skill color-${skill.category}">[${label}]</span> `)
                )
            }
            lists[conversation.type].append(option)
        }
    }
    window.state.show_conditions = original_show_conditions

    $('#loading').hide()
}

function showRoot() {
    window.state.conversation_id = null
    window.state.node_id = null
    window.state.stored_result = null
    window.currentAuthor = null
    window.currentColor = null

    clearConversation()
    $('#dialogue-browser').hide()
    $('#root').show()
}

function advanceConversation(conversationId, nodeId, roll) {
    $('#dialogue-browser').show()
    $('#root').hide()
    clearOptions()

    let url = `api/conversation/${conversationId}/choose/${nodeId}`
    if (roll != null) {
        url += `?roll=${roll}`
    }
    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(window.state),
        contentType: 'application/json',
        dataType: 'json'}
    ).done(function (result) {
        // Coming from root?
        if (window.state.conversation_id == null) {
            clearConversation()
        }

        window.state = result.state
        applyState()
        appendToConversation(result.dialogue)
        setOptions(result.options, result.continue_option)

        document.getElementById('dialogue-browser').scrollIntoView({behavior: 'smooth', block: 'end'})
    })
}

function clearConversation() {
    $('#conversation').empty()
}

function appendToConversation(blocks) {
    $('#conversation').append(buildDialogueBlocks(blocks))
}

function buildDialogueBlocks(blocks) {
    return blocks.map(block => {
        const paragraph = $('<p></p>')
        if (block.difficulty_descriptor != null || block.author !== window.currentAuthor || block.color !== window.currentColor) {
            paragraph.append($('<span></span>').addClass(`author color-${block.color ?? 0}`).text(block.author))
            if (block.difficulty_descriptor != null && block.success != null) {
                const success = block.success ? 'Success' : 'Failure'
                paragraph.append(
                    $('<span class="check-result"></span>').text(` [${block.difficulty_descriptor}: ${success}]`)
                )
            }
            paragraph.append($('<span></span>').text(` – ${block.text}`))
        } else {
            paragraph.append($('<span></span>').text(block.text))
        }
        window.currentAuthor = block.author
        window.currentColor = block.color
        return paragraph
    })
}

function clearOptions() {
    const optionsList = $('#options')
    optionsList.empty()
}

function setOptions(options, continueOption = null) {
    clearOptions()
    if (continueOption !== null) {
        $('#continue-text').text(continueOption.text).removeClass('end')
        $('#continue-button').attr('href', `#/${continueOption.conversation_id}/${continueOption.node_id}`).show()
    } else if (options.length === 0) {
        $('#continue-text').text('End').addClass('end')
        $('#continue-button').attr('href', '#/').show()
    } else {
        $('#continue-button').hide()
        const optionsList = $('#options')
        options.forEach(
            item => {
                optionsList.append(
                    buildOption(
                        item.conversation_id,
                        item.node_id,
                        item.text,
                        item.type,
                        item.condition,
                        item.cost,
                        item.skill,
                        item.difficulty,
                        item.difficulty_descriptor
                    )
                )
            }
        )
    }
}

function buildOption(
    conversationId,
    nodeId,
    text,
    type = 'regular',
    condition = null,
    cost = null,
    skill_id = null,
    difficulty = null,
    difficultyDescriptor = null
) {
    const linkItem = $('<a></a>').prop('href', `#/${conversationId}/${nodeId}`)
    linkItem.append($('<span></span>').text(text))
    const listItem = $('<li></li>')
    if (cost != null) {
        linkItem.prepend(
            $(`<span class="price">[Cost: <span class="currency">✤</span> ${(cost/100).toFixed(2)}] </span>`)
        )
        linkItem.addClass('option-cost')
    }
    if (type === 'red') {
        linkItem.addClass('option-red')
    } else if (type === 'white') {
        linkItem.addClass('option-white')
    }

    if (type === 'red' || type === 'white') {
        const successButton = $('<a></a>').text('Success').prop('href', `#/${conversationId}/${nodeId}/success`)
        const failureButton = $('<a></a>').text('Failure').prop('href', `#/${conversationId}/${nodeId}/failure`)
        const rollBox = $('<div></div>').addClass('roll').append([successButton, failureButton]).hide()
        listItem.prepend(rollBox)
        linkItem.on('click', e => { e.preventDefault(); rollBox.show(); })

        if (skill_id != null && difficulty != null && difficultyDescriptor != null) {
            const skill = SKILLS[skill_id]
            linkItem.text(`[${skill.label} - ${difficultyDescriptor} ${difficulty}] ${linkItem.text()}`)
        }
    }

    if (window.state.show_conditions && condition != null) {
        linkItem.append('<br />').append($('<span></span>').addClass('condition').text(condition))
    }

    listItem.append(linkItem)
    return listItem
}

function setupVariableInputs() {
    for (const attribute of STATE_SIMPLE_ATTRIBUTES) {
        $(`#${attribute}`).click(function () {
            const elem = $(this)
            if (elem.prop('type') === 'checkbox') {
                window.state[attribute] = elem.prop('checked')
            } else {
                window.state[attribute] = parseInt(elem.val())
            }
        })
    }

    const skillIdPrefix = 'skill-'
    $(`[id^=${skillIdPrefix}]`).click(function () {
        const elem = $(this)
        window.state.skills[elem.prop('id').substring(skillIdPrefix.length)] = parseInt(elem.val())
    })

    const itemsBody = $('#items tbody')
    for (const name of window.items.sort()) {
        const nameColumn = $('<td></td>').text(name)
        const ownedInput = $('<input type="checkbox" class="owned" />').prop('id', `owned-${name}`).click(function () {
            updateItemCollection(window.state.items, name, $(this).prop('checked'))
        })
        const ownedColumn = $('<td></td>').append(ownedInput)
        const equippedInput = $('<input type="checkbox" class="equipped" />').prop('id', `equipped-${name}`).click(
            function () {
                updateItemCollection(window.state.equipped, name, $(this).prop('checked'))
            })
        const equippedColumn = $('<td></td>').append(equippedInput)
        itemsBody.append($('<tr></tr>').append(nameColumn).append(ownedColumn).append(equippedColumn))
    }

    // TODO This is too big a drain on performance right now, disable it
    // const variablesContainer = $('#variables')
    // for (const name of Object.keys(window.variables).sort()) {
    //     const type = window.variables[name]
    //     const variableInputContainer = $('<div></div>').addClass('state-property')
    //     variableInputContainer.append($('<label></label>').addClass('variable-label').attr('for', `variable-${name}`).text(`${name}: `))
    //     const variableInput = $('<input />').attr('id', `variable-${name}`)
    //     if (type === 'int') {
    //         variableInput.attr('type', 'number').val(0)
    //     } else if (type === 'bool') {
    //         variableInput.attr('type', 'checkbox')
    //     } else {
    //         console.error(`Invalid type: ${type}`)
    //         continue
    //     }
    //     variableInputContainer.append(variableInput)
    //     variablesContainer.append(variableInputContainer)
    // }
}

function applyState() {
    for (const attribute of STATE_SIMPLE_ATTRIBUTES) {
        const attributeElem = $(`#${attribute}`)
        if (attributeElem.prop('type') === 'checkbox') {
            attributeElem.prop('checked', window.state[attribute])
        } else {
            attributeElem.val(window.state[attribute])
        }
    }

    for (const [skill, value] of Object.entries(window.state.skills)) {
        $(`#skill-${skill}`).val(value)
    }

    $('.owned').val(false)
    for (const item of window.state.items) {
        $(`#owned-${item}`).prop('checked', true)
    }

    $('.equipped').val(false)
    for (const item of window.state.equipped) {
        $(`#equipped-${item}`).val('checked', true)
    }

    // for (const [variable, type] of Object.entries(window.variables)) {
    //     let value = null
    //     if (type === 'int') {
    //         value = 0
    //     } else if (type === 'bool') {
    //         value = false
    //     }
    //     if (window.state.variables.hasOwnProperty(variable)) {
    //         value = window.state.variables[variable]
    //     }
    //
    //     const variableElem = $(`#variable-${variable.replaceAll('.', '\\.')}`)
    //     if (type === 'int') {
    //         variableElem.val(value)
    //     } else if (type === 'bool') {
    //         variableElem.prop('checked', value)
    //     }
    // }
}

function updateItemCollection(itemCollection, name, itemState) {
    if (itemState) {
        if (!itemCollection.includes(name)) {
            itemCollection.push(name)
        }
    } else {
        const ownedIdx = itemCollection.indexOf(name)
        if (ownedIdx > -1) {
            itemCollection.splice(ownedIdx, 1)
        }
    }
}

init();
