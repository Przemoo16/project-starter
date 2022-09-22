import * as yup from 'yup';

import { t } from '../../i18n';

export const getLoginSchema = () =>
  yup.object().shape({
    email: yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
    password: yup.string().required(t('validation.required')),
  });

export const getRegisterSchema = (
  nameMinLength: number,
  nameMaxLength: number,
  passwordMinLength: number,
  passwordMaxLength: number,
) => {
  return yup.object().shape({
    name: yup
      .string()
      .required(t('validation.required'))
      .min(nameMinLength, t('validation.minName', { min: nameMinLength }))
      .max(nameMaxLength, t('validation.maxName', { max: nameMaxLength })),
    email: yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
    password: yup
      .string()
      .required(t('validation.required'))
      .min(passwordMinLength, t('validation.minPassword', { min: passwordMinLength }))
      .max(passwordMaxLength, t('validation.maxPassword', { max: passwordMaxLength })),
    repeatPassword: yup.string().oneOf([yup.ref('password'), null], t(`validation.passwordMatch`)),
  });
};

export const getResetPasswordSchema = () =>
  yup.object().shape({
    email: yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
  });

export const getSetPasswordSchema = (passwordMinLength: number, passwordMaxLength: number) => {
  return yup.object().shape({
    password: yup
      .string()
      .required(t('validation.required'))
      .min(passwordMinLength, t('validation.minPassword', { min: passwordMinLength }))
      .max(passwordMaxLength, t('validation.maxPassword', { max: passwordMaxLength })),
    repeatPassword: yup.string().oneOf([yup.ref('password'), null], t(`validation.passwordMatch`)),
  });
};
