import React from 'react';
import ReactDOM from 'react-dom';
import _ from 'lodash';
import {
  Glyphicon,
  Row,
  Col,
  FormControl,
  Button,
  ButtonGroup,
  InputGroup,
  FormGroup,
  MenuItem,
  DropdownButton,
  Badge,
  Checkbox,
  Radio,
  Popover,
  Overlay,
  Nav,
  NavItem,
  ControlLabel,
  Form,
  Tabs,
  Tab,
  HelpBlock,
  ToggleButtonGroup,
  ToggleButton,
} from 'react-bootstrap';

import $ from 'jquery';
import * as constants from './constants';

const selectionConstants = constants.PROTOCOL_CONSTANTS.front_to_back;
const supply_suggestions_prefix = 'supply_suggestions';

function getSelectionInfo(originalMessages) {
  // This function determines which KB reply is currently in the
  // <selected> and <compare to> state.

  let selectedMessage = null;
  let compareToMessage = null;

  const extractIdFromCommandMsg = message => {
    const {
      select_kb_entry_prefix,
      select_reference_kb_entry_prefix,
    } = selectionConstants;

    const prefix =
      message.indexOf(select_kb_entry_prefix) > -1
        ? select_kb_entry_prefix
        : select_reference_kb_entry_prefix;

    const message_id_content_separator_position = message.indexOf('|');

    return message
      .slice(prefix.length, message_id_content_separator_position)
      .trim();
  };

  // Iterate through all messages to find
  // the most recent, selected KB messages.
  for (const msg of originalMessages) {
    if (msg.text.startsWith(selectionConstants.select_kb_entry_prefix)) {
      selectedMessage = extractIdFromCommandMsg(msg.text);
      if (selectedMessage === compareToMessage) {
        // If a message was selected which was previously "compared to",
        // compareToMessage needs to be cleared. Otherwise, the compared-to
        // state will be restored when a new message will be selected
        compareToMessage = null;
      }
    } else if (
      msg.text.startsWith(selectionConstants.select_reference_kb_entry_prefix)
    ) {
      compareToMessage = extractIdFromCommandMsg(msg.text);
      if (compareToMessage === selectedMessage) {
        // If a message was selected to be "compared to" and that message was previously selected,
        // selectedMessage needs to be cleared. Otherwise, the selected state will be restored when
        // a new message will be compared-to
        selectedMessage = null;
      }
    } else if (msg.id === 'KnowledgeBase') {
      selectedMessage = msg.message_id;
    }
  }

  return {
    selectedMessage,
    compareToMessage,
  };
}

function KnowledgeBaseMessage(props) {
  const { message, selectionInfo } = props;

  const needle = 'Example: ';
  const needlePosition = message.indexOf(needle);

  const { selectedMessage, compareToMessage } = selectionInfo;

  let toggleValue;
  if (props.message_id === selectedMessage) {
    toggleValue = 'selected';
  } else if (props.message_id === compareToMessage) {
    toggleValue = 'compare_to';
  } else {
    toggleValue = 'not_selected';
  }

  if (needlePosition === -1) {
    return message;
  }

  const regex = /Found ([0-9\-]+)/;
  let count = null;
  const m = regex.exec(message);
  if (m != null) {
    // The result can be accessed through the `m`-variable.
    count = m[1];
  }
  let exampleJson;
  try {
    exampleJson = JSON.parse(message.slice(needlePosition + needle.length, -1));
  } catch (exc) {
    console.log('Failed to parse example JSON.');
  }
  if (exampleJson != null) {
    const rows = Object.keys(exampleJson).map((key, idx) => {
      if (key === 'api_name') {
        // This is for internal processing only, so don't show it
        return;
      }

      // Split CamelCase string into spaced string
      let long_key = key.replace(/([a-z0-9])([A-Z])/g, '$1 $2');

      let value = exampleJson[key];
      if (typeof value === 'boolean') {
        value = value ? 'yes' : 'no';
      } else if (Array.isArray(value)) {
        if (value.length > 2 || key === 'Walking Instructions') {
          //           ab = (key === 'Walking Instructions') ? 'a' : 'b';
          // Long lists should be shown as numbered lists
          return (
            <tr valign="top" key={key}>
              <td style={{ paddingRight: 10 }}>{long_key}:</td>
              <td width="400px">
                <ol>
                  {value.map(el => (
                    <li>{el.trim()}</li>
                  ))}
                </ol>
              </td>
            </tr>
          );
        } else {
          // Short lists are comma separated
          value = value.join(', ');
        }
      }

      return (
        <tr valign="top" key={key}>
          <td style={{ paddingRight: 10 }}>{long_key}:</td>
          <td width="400px">{value}</td>
        </tr>
      );
    });

    const handleSelection = value => {
      if (value === 'not_selected') {
        return;
      }

      const prefix =
        value === 'selected'
          ? selectionConstants.select_kb_entry_prefix
          : selectionConstants.select_reference_kb_entry_prefix;

      const example_string = message.slice(needlePosition + needle.length, -1);

      props.onMessageSend(
        `${prefix} ${props.message_id}|${example_string}`,
        {},
        () => console.log('sent selection')
      );
    };

    return (
      <div>
        {count > 1 ? <span>This and {count - 1} matches exist:</span> : null}
        <table style={{ borderStyle: 'none' }}>
          <tbody>{rows}</tbody>
        </table>
        <br />

        <ToggleButtonGroup
          type="radio"
          name="options"
          value={toggleValue}
          onChange={handleSelection}
        >
          <ToggleButton value={'selected'}>selected</ToggleButton>
          <ToggleButton
            value={'compare_to'}
            disabled={toggleValue === 'selected'}
            title={
              toggleValue === 'selected'
                ? "Cannot compare to this message because it's already selected."
                : null
            }
          >
            compare to
          </ToggleButton>
          <ToggleButton
            value={'not_selected'}
            disabled
            title={
              'Deselect this entry by selecting another knowledge base item.'
            }
          >
            not selected
          </ToggleButton>
        </ToggleButtonGroup>
      </div>
    );
  }

  return message;
}

class ChatMessage extends React.Component {
  constructor(props) {
    super(props);
    this.state = { textval: '', sending: false };
  }

  handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.props.onMessageSend(this.state.textval, {}, () =>
        this.setState({ textval: '', sending: false })
      );

      e.stopPropagation();
      e.nativeEvent.stopImmediatePropagation();
    }
  }

  updateValue(value) {
    this.setState({ textval: '' + value });
  }

  render() {
    let float_loc = 'left';
    let alert_class = 'alert-warning';
    if (this.props.is_self) {
      float_loc = 'right';
      alert_class = 'alert-info';
    }
    let duration = null;
    if (this.props.duration !== undefined) {
      let duration_seconds = Math.floor(this.props.duration / 1000) % 60;
      let duration_minutes = Math.floor(this.props.duration / 60000);
      let min_text = duration_minutes > 0 ? duration_minutes + ' min' : '';
      let sec_text = duration_seconds > 0 ? duration_seconds + ' sec' : '';
      duration = (
        <small>
          <br />
          <i>Duration: </i>
          {min_text + ' ' + sec_text}
        </small>
      );
    }

    const isKB = this.props.agent_id === 'KnowledgeBase';
    const isSYS = this.props.agent_id === 'MTurk System';
    let message = null;

    if (this.props.isSuggestionMessage) {
      // TODO (low-pri): if the backend provides JSON instead, we can use JSON.parse()
      const suggestions = eval(
        this.props.command.slice(supply_suggestions_prefix.length)
      );

      message = (
        <div>
          Please pick one of the following replies:
          {suggestions.map(suggestion => (
            <div style={{ margin: '6px 0' }}>
              <Button
                className="btn"
                onClick={() => {
                  this.props.onMessageSend(
                    `${selectionConstants.pick_suggestion_prefix}${suggestion}`,
                    {},
                    () => console.log('Sent suggestion')
                  );
                }}
              >
                <p
                  style={{
                    width: '360px',
                    margin: '0',
                    wordBreak: 'normal',
                    whiteSpace: 'normal',
                  }}
                >
                  {suggestion}
                </p>
              </Button>
            </div>
          ))}
          <FormControl
            type="text"
            id="id_text_input"
            style={{
              width: '80%',
              height: '100%',
              float: 'left',
              fontSize: '16px',
            }}
            value={this.state.textval}
            placeholder="Optional: Enter free-form reply here..."
            onKeyPress={e => this.handleKeyPress(e)}
            onChange={e => this.updateValue(e.target.value)}
          />
          <Button
            className="btn btn-primary"
            id="id_send_msg_button"
            disabled={this.state.textval == ''}
            onClick={() =>
              this.props.onMessageSend(this.state.textval, {}, () =>
                this.setState({ textval: '', sending: false })
              )
            }
          >
            Send
          </Button>
        </div>
      );
    } else if (isKB) {
      message = <KnowledgeBaseMessage {...this.props} />;
    } else {
      message = this.props.message;
    }
    const onlyVisibleMsg = isKB || isSYS ? ' (Only visible to you)' : null;

    let msg_color = undefined;
    if (isKB) {
      msg_color = '#f4cdcc'; // light red
    } else if (isSYS) {
      msg_color = '#FDEFB6'; // light yellow
    }

    return (
      <div
        className={'row'}
        style={{
          marginLeft: '0',
          marginRight: '0',
          backgroundColor: this.props.invisible ? '#ff2300cf' : 'default',
        }}
      >
        <div
          className={'alert ' + alert_class}
          role="alert"
          style={{
            float: float_loc,
            display: 'table',
            backgroundColor: msg_color,
            color: onlyVisibleMsg ? 'rgb(88, 90, 94)' : undefined,
          }}
        >
          <span style={{ fontSize: '16px', whiteSpace: 'pre-wrap' }}>
            <b>
              {this.props.agent_id}
              {onlyVisibleMsg}
            </b>
            : {message}
          </span>
          {duration}
        </div>
      </div>
    );
  }
}

export class MessageList extends React.Component {
  makeMessages() {
    let agent_id = this.props.agent_id;
    let messages = this.props.messages;
    // Handles rendering messages from both the user and anyone else
    // on the thread - agent_ids for the sender of a message exist in
    // the m.id field.

    const selectionInfo = getSelectionInfo(this.props.messages);

    function shouldNotRender(m) {
      if (
        m.command != null &&
        !m.command.startsWith(supply_suggestions_prefix)
      ) {
        return true;
      }

      if (m.text.startsWith('?')) {
        return true;
      }

      if (m.text.startsWith('<') && m.text.indexOf('>') > -1) {
        return true;
      }

      return false;
    }

    return messages.map((m, idx) => {
      const isSuggestionMessage =
        m.command != null && m.command.startsWith(supply_suggestions_prefix);

      const dontRender =
        shouldNotRender(m) ||
        (isSuggestionMessage && idx != messages.length - 1);

      return dontRender &&
        !constants.DEBUG_FLAGS.RENDER_INVISIBLE_MESSAGES ? null : (
        <div key={m.message_id}>
          <ChatMessage
            {...this.props}
            is_self={m.id == agent_id}
            invisible={dontRender}
            agent_id={m.id === 'Wizard' ? 'AI Assistant' : m.id}
            message={m.text}
            command={m.command}
            task_data={m.task_data}
            message_id={m.message_id}
            duration={this.props.is_review ? m.duration : undefined}
            selectionInfo={selectionInfo}
            isSuggestionMessage={isSuggestionMessage}
          />
        </div>
      );
    });
  }

  render() {
    return (
      <div id="message_thread" style={{ width: '100%' }}>
        {this.makeMessages()}
      </div>
    );
  }
}
