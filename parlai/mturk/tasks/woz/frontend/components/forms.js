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
} from 'react-bootstrap';
import * as constants from './constants';

export class QueryForm extends React.Component {
  constructor(props) {
    super(props);
    this.addFormFieldRef = React.createRef();
    this.formFieldIdCounter = 0;

    // A formField is
    // {
    //    fieldName: string,
    //    id: number
    //    operatorValue: string,
    //    value: string
    // }

    this.state = {
      addedFormFields: [],
      formFieldData: {},
    };
  }

  addFormField = fieldName => {
    const id = this.formFieldIdCounter++;
    this.setState({
      addedFormFields: [...this.state.addedFormFields, { fieldName, id }],
    });
  };

  removeFormField = fieldId => {
    this.setState({
      addedFormFields: this.state.addedFormFields.filter(fieldNameWithId => {
        return fieldNameWithId.id !== fieldId;
      }),
    });
  };

  onChangeValue = newFormField => {
    this.setState({
      formFieldData: {
        ...this.state.formFieldData,
        [newFormField.id]: newFormField,
      },
    });
  };

  deriveFormDatumFromDOM(form, formFieldId) {
    const formDatum = {
      id: formFieldId,
      fieldName: null,
      value: null,
      operatorValue: null,
    };

    for (const element of form.elements) {
      if (element.getAttribute('data-form-field-id') !== `${formFieldId}`) {
        continue;
      }
      if (element.getAttribute('data-is-operator') === 'true') {
        formDatum.operatorValue = element.value;
      } else {
        formDatum.fieldName = element.getAttribute('data-field-name');

        if (element.type === 'checkbox') {
          formDatum.value = element.checked;
        } else if (element.type === 'select-one') {
          formDatum.value = element.value;
        } else if (element.type === 'number') {
          formDatum.value = element.value;
        } else if (element.type === 'select-multiple') {
          const selectedOptions = Array.from(
            element.querySelectorAll('option:checked'),
            e => e.value
          );
          formDatum.value = selectedOptions;
        }
      }
    }

    return formDatum;
  }

  onSubmit = (event, relevantFormFields) => {
    console.log(this.state.formFieldData);
    event.preventDefault();
    const form = event.target;

    const constraints = [];

    for (const formFieldWithId of Object.values(relevantFormFields)) {
      let formField = this.state.formFieldData[formFieldWithId.id];
      if (!formField) {
        formField = this.deriveFormDatumFromDOM(form, formFieldWithId.id);
      }

      let operator = formField.operatorValue;
      if (formField.fieldName === 'RequestType') {
        // Johannes: Dirty bug fix
        operator = null;
      }
      const operatorWrapper =
        operator == null ? val => val : val => `api.${operator}(${val})`;

      let value = formField.value;
      if (typeof value === 'boolean') {
        value = value ? 'True' : 'False';
      } else if (isNaN(value)) {
        value = JSON.stringify(value);
      } else {
        value = value;
      }

      constraints.push({
        [formField.fieldName]: `${operatorWrapper(value)}`,
      });
    }

    console.log('constraints', constraints);
    //    const queryString = `? ${JSON.stringify(constraints)}`;
    const queryString = `? ${JSON.stringify({
      db: this.props.category,
      constraints,
    })}`;
    console.log('sending', queryString);
    this.props.onMessageSend(queryString, {}, () => console.log('done'));
  };

  render() {
    const { category, formDescriptionIndex, formDescription } = this.props;

    const { addFormField, removeFormField } = this;

    // TODO (low-pri): remove this flag
    const use_mock = false;
    const json = use_mock ? apartmentJson : formDescription;

    const activeAndRequiredFormFields = json.required
      .map(fieldName => ({
        fieldName,
        id: fieldName,
        operatorValue: null,
        value: null,
      }))
      .concat(this.state.addedFormFields);

    return (
      <form
        onSubmit={event => this.onSubmit(event, activeAndRequiredFormFields)}
      >
        <FormGroup>
          <div>
            <FormControl
              componentClass="select"
              style={{ maxWidth: 130, display: 'inline-block' }}
              ref={this.addFormFieldRef}
            >
              {json.input.map(input => (
                <option value={input.Name}>{input.Name}</option>
              ))}
            </FormControl>
            <Button
              className="btn"
              onClick={() => {
                const domNode = ReactDOM.findDOMNode(
                  this.addFormFieldRef.current
                );
                addFormField(domNode.value);
              }}
              style={{ marginLeft: 20 }}
            >
              Add Constraint
            </Button>
          </div>
        </FormGroup>
        <hr />
        {jsonToForm(
          json,
          activeAndRequiredFormFields,
          removeFormField,
          this.state.formFieldData,
          this.onChangeValue
        )}

        <Button
          className="btn btn-primary"
          disabled={this.props.chat_state !== 'text_input'}
          type="submit"
        >
          Query
        </Button>
      </form>
    );
  }
}

function FieldGroup({ id, label, help, ...props }) {
  return (
    <FormGroup controlId={id}>
      <ControlLabel>{label}</ControlLabel>
      <FormControl {...props} />
      {help && <HelpBlock>{help}</HelpBlock>}
    </FormGroup>
  );
}

function ControlLabelWithRemove(props) {
  return (
    <ControlLabel>
      {props.formFieldName}
      <Button
        style={{ border: 0, padding: '3px 6px', background: 'transparent' }}
        onClick={() => props.onRemove(props.formFieldId)}
      >
        <Glyphicon glyph="remove" />
      </Button>
    </ControlLabel>
  );
}

export function jsonToForm(
  json,
  activeFormFields,
  removeFormField,
  formFieldData,
  onChangeValue
) {
  const inputByName = _.keyBy(json.input, 'Name');
  return activeFormFields.map(formFieldWithId => {
    const formFieldName = formFieldWithId.fieldName;
    const formFieldId = formFieldWithId.id;

    const input = inputByName[formFieldName];
    console.log(formFieldName);
    console.log(input);
    const isRequired = json.required.indexOf(input.Name) >= 0;
    const controlLabelWithRemove = (
      <ControlLabelWithRemove
        formFieldName={input['ReadableName']}
        formFieldId={formFieldId}
        onRemove={removeFormField}
      />
    );
    //    console.log(controlLabelWithRemove);

    const formFieldDatum = formFieldData[formFieldId] || {
      id: formFieldId,
      fieldName: formFieldName,
      value: null,
      operatorValue: input.Type === 'CategoricalMultiple' ? 'contains' : null,
    };

    switch (input.Type) {
      case 'LongString': {
        return (
          <FormGroup>
            {controlLabelWithRemove}
            <FormControl
              required={isRequired}
              name={formFieldId}
              data-form-field-id={formFieldDatum.id}
              data-is-operator={false}
              data-field-name={formFieldDatum.fieldName}
              componentClass="textarea"
              placeholder="textarea"
              value={formFieldDatum.value}
              onChange={event =>
                onChangeValue({
                  ...formFieldDatum,
                  value: event.target.value,
                })
              }
            />
          </FormGroup>
        );
      }
      case 'ShortString': {
        return (
          <FormGroup>
            {controlLabelWithRemove}
            <FormControl
              name={formFieldId}
              required={isRequired}
              data-form-field-id={formFieldDatum.id}
              data-is-operator={false}
              data-field-name={formFieldDatum.fieldName}
              componentClass="input"
              style={{ maxWidth: 400 }}
              value={formFieldDatum.value}
              onChange={event =>
                onChangeValue({
                  ...formFieldDatum,
                  value: event.target.value,
                })
              }
            />
          </FormGroup>
        );
      }
      case 'RequestType':
      case 'Categorical':
      case 'CategoricalMultiple': {
        const uiLogicInfo = {
          RequestType: {
            is_equal_to: 'SingleSelect',
          },
          Categorical: {
            is_equal_to: 'SingleSelect',
            is_one_of: 'MultiSelect',
            // Todo: Probably easier if the back-end provides "is_not_equal" ?
            // is_unequal_to: 'SingleSelect',  // Johannes: These have no effect
            // is_not: 'MultiSelect',
          },
          CategoricalMultiple: {
            contains: 'SingleSelect',
            contain_all_of: 'MultiSelect',
            contain_at_least_one_of: 'MultiSelect',
            contains_not: 'SingleSelect',
          },
        }[input.Type];

        const operatorUi = (
          <FormControl
            componentClass="select"
            placeholder={Object.keys(uiLogicInfo)[0]}
            style={{ maxWidth: 130, display: 'inline-block' }}
            data-form-field-id={formFieldDatum.id}
            data-is-operator={true}
            data-field-name={formFieldDatum.fieldName}
            value={formFieldDatum.operatorValue}
            onChange={event =>
              onChangeValue({
                ...formFieldDatum,
                operatorValue: event.target.value,
              })
            }
          >
            {Object.keys(uiLogicInfo).map(key => (
              <option value={key}>{key.replace(/_/g, ' ')}</option>
            ))}
          </FormControl>
        );

        const isMultiple =
          uiLogicInfo[formFieldDatum.operatorValue] === 'MultiSelect';

        return (
          <FormGroup>
            {controlLabelWithRemove}
            <div>
              {operatorUi}
              <FormControl
                required={isRequired}
                name={formFieldId}
                componentClass="select"
                placeholder="select"
                data-form-field-id={formFieldDatum.id}
                data-is-operator={false}
                data-field-name={formFieldDatum.fieldName}
                multiple={isMultiple}
                value={formFieldDatum.value}
                onChange={event => {
                  if (event.target.multiple) {
                    const selectedOptions = Array.from(
                      event.target.querySelectorAll('option:checked'),
                      e => e.value
                    );
                    onChangeValue({
                      ...formFieldDatum,
                      value: selectedOptions,
                    });
                  } else {
                    onChangeValue({
                      ...formFieldDatum,
                      value: event.target.value,
                    });
                  }
                }}
                style={{
                  maxWidth: 200,
                  display: 'inline-block',
                  verticalAlign: 'top',
                  marginLeft: 10,
                }}
              >
                {input.Categories.map((category, idx) => (
                  <option key={`${category}-idx`} value={category}>
                    {category}
                  </option>
                ))}
              </FormControl>
            </div>
          </FormGroup>
        );
      }
      case 'Boolean': {
        return (
          <FormGroup>
            <Checkbox
              name={formFieldId}
              required={isRequired}
              value={formFieldDatum.value}
              data-form-field-id={formFieldDatum.id}
              data-is-operator={false}
              data-field-name={formFieldDatum.fieldName}
              onChange={event =>
                onChangeValue({
                  ...formFieldDatum,
                  value: event.target.checked,
                })
              }
              inline
            >
              {input.Name}
            </Checkbox>
            <Button
              style={{
                border: 0,
                padding: '3px 6px',
                background: 'transparent',
              }}
              onClick={() => removeFormField(formFieldId)}
            >
              <Glyphicon glyph="remove" />
            </Button>
          </FormGroup>
        );
      }
      case 'Integer': {
        // TODO (high-pri): more operators for all data types

        const { Min, Max } = input;

        return (
          <FormGroup controlId="formControlsNumber">
            {controlLabelWithRemove}
            <div>
              <FormControl
                required={isRequired}
                componentClass="select"
                data-form-field-id={formFieldDatum.id}
                data-is-operator={true}
                data-field-name={formFieldDatum.fieldName}
                style={{ maxWidth: 180, display: 'inline-block' }}
                value={formFieldDatum.operatorValue}
                onChange={event =>
                  onChangeValue({
                    ...formFieldDatum,
                    operatorValue: event.target.value,
                  })
                }
              >
                <option value="is_equal_to">is equal to</option>
                <option value="is_greater_than">is greater than</option>
                <option value="is_at_least">is at least</option>
                <option value="is_at_most">is at most</option>
                <option value="is_less_than">is less than</option>
                <option value="is_not">is not</option>
              </FormControl>
              <FormControl
                required={isRequired}
                name={formFieldId}
                data-form-field-id={formFieldDatum.id}
                data-is-operator={false}
                data-field-name={formFieldDatum.fieldName}
                componentClass="input"
                type="number"
                min={Min}
                max={Max}
                style={{
                  maxWidth: 150,
                  display: 'inline-block',
                  marginLeft: 20,
                }}
                value={formFieldDatum.value}
                onChange={event =>
                  onChangeValue({
                    ...formFieldDatum,
                    value: parseFloat(event.target.value),
                  })
                }
              />
            </div>
          </FormGroup>
        );
      }
    }
  });
}
