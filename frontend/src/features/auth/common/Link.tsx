import { Link as BaseLink, LinkProps as BaseLinkProps } from '../../../ui-components/Link';

type LinkProps = Omit<BaseLinkProps, 'underline' | 'variant'>;

export const Link = (props: LinkProps) => <BaseLink underline="hover" variant="body2" {...props} />;
