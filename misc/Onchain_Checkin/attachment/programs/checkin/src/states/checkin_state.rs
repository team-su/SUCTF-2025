use anchor_lang::prelude::*;

#[account]
pub struct CheckinState {
    pub flag3: Pubkey,
}

impl Space for CheckinState {
    const INIT_SPACE: usize = 8 + 32;
}
