{{/*
Определяем название приложения
Будет использоваться в качестве названия для ресурсов
Если название чарта .Chart.Name содерджится в релизе
то используем название релиза
Иначе название приложения будет составное
из названий чарта и релиза
*/}}
{{- define "chart.fullname" -}}
{{- if contains .Chart.Name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Chart.Name .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Селекторные метки для компонентов
*/}}
{{- define "chart.selectorLabels" -}}
app: {{ .Chart.Name }}
release: {{ .Release.Name }}
{{- end }}

{{/*
Общие метки для компонентов
*/}}
{{- define "chart.labels" -}}
{{- $appVersion := default .Values.image.tag $.Chart.AppVersion }}
chart: {{ printf "%s-%s" .Chart.Name $appVersion }}
version: {{ $appVersion | quote }}
{{ include "chart.selectorLabels" . }}
{{- end }}
