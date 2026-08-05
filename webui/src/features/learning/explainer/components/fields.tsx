// src/features/learning/explainer/components/fields.tsx
/**
 * Reusable atomic form fields shared across all Explainer tools.
 * Input/Textarea spread RHF registration props; Select/Slider are wrapped in
 * react-hook-form Controller so tool forms stay declarative and consistent.
 */
"use client";

import type { ReactNode } from "react";
import { Controller, type Control, type FieldValues, type Path } from "react-hook-form";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { cn } from "@/lib/utils";

export interface FieldOption {
  value: string;
  label: string;
}

interface FieldWrapProps {
  label: string;
  htmlFor: string;
  error?: string;
  hint?: string;
  children: ReactNode;
}

function FieldWrap({ label, htmlFor, error, hint, children }: FieldWrapProps) {
  return (
    <div className="space-y-1.5">
      <Label htmlFor={htmlFor} className="text-sm font-medium">
        {label}
      </Label>
      {children}
      {error ? (
        <p className="text-xs text-destructive">{error}</p>
      ) : hint ? (
        <p className="text-xs text-muted-foreground">{hint}</p>
      ) : null}
    </div>
  );
}

interface InputFieldProps extends React.ComponentProps<typeof Input> {
  label: string;
  htmlFor: string;
  error?: string;
  hint?: string;
}

export function InputField({
  label,
  htmlFor,
  error,
  hint,
  className,
  ...props
}: InputFieldProps) {
  return (
    <FieldWrap label={label} htmlFor={htmlFor} error={error} hint={hint}>
      <Input
        id={htmlFor}
        aria-invalid={!!error}
        className={cn("bg-transparent", className)}
        {...props}
      />
    </FieldWrap>
  );
}

interface TextareaFieldProps extends React.ComponentProps<typeof Textarea> {
  label: string;
  htmlFor: string;
  error?: string;
  hint?: string;
}

export function TextareaField({
  label,
  htmlFor,
  error,
  hint,
  className,
  ...props
}: TextareaFieldProps) {
  return (
    <FieldWrap label={label} htmlFor={htmlFor} error={error} hint={hint}>
      <Textarea
        id={htmlFor}
        aria-invalid={!!error}
        className={cn("min-h-20 resize-none bg-transparent", className)}
        {...props}
      />
    </FieldWrap>
  );
}

interface SelectFieldProps<TFieldValues extends FieldValues> {
  label: string;
  name: Path<TFieldValues>;
  htmlFor: string;
  control: Control<TFieldValues>;
  options: FieldOption[];
  error?: string;
  hint?: string;
  disabled?: boolean;
  placeholder?: string;
}

export function SelectField<TFieldValues extends FieldValues>({
  label,
  name,
  htmlFor,
  control,
  options,
  error,
  hint,
  disabled,
  placeholder = "Select an option",
}: SelectFieldProps<TFieldValues>) {
  return (
    <FieldWrap label={label} htmlFor={htmlFor} error={error} hint={hint}>
      <Controller
        name={name}
        control={control}
        render={({ field }) => (
          <Select value={field.value} onValueChange={field.onChange} disabled={disabled}>
            <SelectTrigger id={htmlFor} className="w-full" aria-invalid={!!error}>
              <SelectValue placeholder={placeholder} />
            </SelectTrigger>
            <SelectContent>
              {options.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}
      />
    </FieldWrap>
  );
}

interface SliderFieldProps<TFieldValues extends FieldValues> {
  label: string;
  name: Path<TFieldValues>;
  htmlFor: string;
  control: Control<TFieldValues>;
  min: number;
  max: number;
  step?: number;
  error?: string;
  disabled?: boolean;
  /** Formats the current slider value, e.g. (value) => `${value} yrs`. */
  formatValue?: (value: number) => string;
}

export function SliderField<TFieldValues extends FieldValues>({
  label,
  name,
  htmlFor,
  control,
  min,
  max,
  step = 1,
  error,
  disabled,
  formatValue = (value) => String(value),
}: SliderFieldProps<TFieldValues>) {
  return (
    <FieldWrap label={label} htmlFor={htmlFor} error={error}>
      <div className="flex items-center gap-3 pt-1">
        <Controller
          name={name}
          control={control}
          render={({ field }) => (
            <>
              <Slider
                id={htmlFor}
                min={min}
                max={max}
                step={step}
                value={[field.value]}
                onValueChange={(values) => field.onChange(values[0])}
                disabled={disabled}
                className="flex-1"
              />
              <span className="w-16 shrink-0 rounded-md bg-muted px-2 py-1 text-center text-xs font-medium tabular-nums">
                {formatValue(field.value)}
              </span>
            </>
          )}
        />
      </div>
    </FieldWrap>
  );
}
