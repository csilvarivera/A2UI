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

import { AppConfig } from "./types.js";

export const config: AppConfig = {
  key: "field_service",
  title: "Field Service Assistant",
  heroImage: "/field_service_hero.png",
  heroImageDark: "/field_service_hero_dark.png",
  background: `radial-gradient(
    at 0% 0%,
    light-dark(rgba(200, 230, 255, 0.3), rgba(0, 100, 255, 0.15)) 0px,
    transparent 50%
  ),
  radial-gradient(
    at 100% 0%,
    light-dark(rgba(230, 255, 230, 0.3), rgba(0, 255, 100, 0.15)) 0px,
    transparent 50%
  ),
  radial-gradient(
    at 100% 100%,
    light-dark(rgba(255, 240, 200, 0.3), rgba(255, 150, 0, 0.15)) 0px,
    transparent 50%
  ),
  radial-gradient(
    at 0% 100%,
    light-dark(rgba(255, 200, 200, 0.3), rgba(255, 0, 0, 0.15)) 0px,
    transparent 50%
  ),
  linear-gradient(
    120deg,
    light-dark(#f8f9fa, #121212) 0%,
    light-dark(#e9ecef, #1e1e1e) 100%
  )`,
  placeholder: "I'm at the site to service the Roof-top Unit 4.",
  loadingText: [
    "Identifying asset...",
    "Retrieving maintenance protocol...",
    "Searching parts catalog...",
    "Consulting technical manuals...",
  ],
  serverUrl: "http://localhost:10002",
};
