/*
 Copyright 2025 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 */

import { html, css, nothing } from "lit";
import { customElement, property } from "lit/decorators.js";
import { Root } from "./root.js";
import { StringValue, BooleanValue } from "../types/primitives";
import { classMap } from "lit/directives/class-map.js";
import { A2uiMessageProcessor } from "../data/model-processor.js";
import { styleMap } from "lit/directives/style-map.js";
import { structuralStyles } from "./styles.js";
import { extractStringValue, extractBooleanValue } from "./utils/utils.js";

@customElement("a2ui-checkbox")
export class Checkbox extends Root {
  @property()
  accessor value: BooleanValue | null = null;

  @property()
  accessor label: StringValue | null = null;

  static styles = [
    structuralStyles,
    css`
      * {
        box-sizing: border-box;
      }

      :host {
        display: block;
        flex: var(--weight);
        min-height: 0;
        overflow: auto;
      }

      input {
        display: block;
        width: 100%;
      }

      .description {
        font-size: 14px;
        margin-bottom: 4px;
      }
    `,
  ];

  #setBoundValue(value: string) {
    if (!this.value || !this.processor) {
      return;
    }

    if (!("path" in this.value)) {
      return;
    }

    if (!this.value.path) {
      return;
    }

    this.processor.setData(
      this.component,
      this.value.path,
      value,
      this.surfaceId ?? A2uiMessageProcessor.DEFAULT_SURFACE_ID
    );
  }

  #renderField(value: boolean) {
    return html` <section
        class=${classMap(this.theme.components.CheckBox.container)}
        style=${this.theme.additionalStyles?.CheckBox
        ? styleMap(this.theme.additionalStyles?.CheckBox)
        : nothing}
      >
        <input
          class=${classMap(this.theme.components.CheckBox.element)}
          autocomplete="off"
          @input=${(evt: Event) => {
        if (!(evt.target instanceof HTMLInputElement)) {
          return;
        }

        this.#setBoundValue(evt.target.checked ? "true" : "false");
      }}
          id="data"
          type="checkbox"
          .checked=${value}
        />
        <label class=${classMap(this.theme.components.CheckBox.label)} for="data"
          >${extractStringValue(this.label, this.component, this.processor, this.surfaceId)}</label
        >
      </section>`;
  }

  render() {
    const value = extractBooleanValue(this.value, this.component, this.processor, this.surfaceId);
    return this.#renderField(value);
  }
}
